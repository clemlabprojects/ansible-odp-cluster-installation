#!/usr/bin/env python
'''
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import optparse
from pprint import pprint
import logging
import sys
import math
import ast
import subprocess
import re

''' Reserved for OS + DN + NM,  Map: Memory => Reservation '''
reservedStack = { 4:1, 8:2, 16:2, 24:4, 48:6, 64:8, 72:8, 96:12,
                   128:24, 256:32, 512:64}
''' Reserved for HBase. Map: Memory => Reservation '''

reservedHBase = {4:1, 8:1, 16:2, 24:4, 48:8, 64:8, 72:8, 96:16,
                   128:24, 256:32, 512:64}
GB = 1024

def getMinContainerSize(memory):
  if (memory <= 4):
    return 256
  elif (memory <= 8):
    return 512
  elif (memory <= 24):
    return 1024
  else:
    return 2048
  pass

def getReservedStackMemory(memory):
  if (reservedStack.has_key(memory)):
    return reservedStack[memory]
  if (memory <= 4):
    ret = 1
  elif (memory >= 512):
    ret = 64
  else:
    ret = 1
  return ret

def getReservedHBaseMem(memory):
  if (reservedHBase.has_key(memory)):
    return reservedHBase[memory]
  if (memory <= 4):
    ret = 1
  elif (memory >= 512):
    ret = 64
  else:
    ret = 2
  return ret

def discover_disks():
  disks = []
  result = subprocess.check_output(['df']).splitlines()
  for x in range(1, len(result)):
    s = result[x]
    if s.find('map') != -1 :
      continue
    line = re.compile("\s+").split(s)
    disk = {}
    properties = ['filesystem', 'total', 'used', 'available', 'available_pourcent', 'mountpoint']
    for i in range(0, len(properties)):
      disk[properties[i]] = line[i]
    disk['total'] = int(disk['total'].strip(),10) * 1024
    disk['used'] = int(disk['used'].strip(),10) * 1024
    disk['available'] = int(disk['available'].strip(),10) * 1024
    if (disk['filesystem'].find('/data') > -1) or (disk['filesystem'].find('/grid') > -1):
        disks.append(disk)
  return disks

def discover_cores():
  cpus = []
  result = subprocess.check_output(['cat','/proc/cpuinfo']).splitlines()
  cpu = {}
  for x in range(1, len(result)):
    line = result[x].strip()
    if line == '':
      if len(cpu.keys()) > 0 :
        cpus.append(cpu)
        cpu = {}
    else:
      parts = line.split(':')
      cpu[parts[0].strip()] = parts[1].strip()
  return cpus

def discover_memory():
  memoryinfo = {}
  result = subprocess.check_output(['cat','/proc/meminfo']).splitlines()
  for x in range(0, len(result)):
    line = result[x]
    if line != '':
      data = line.split(':')
      property = data[0].strip()
      parts = data[1].strip().split(' ')
      if len(parts) > 1 :
        value, unit = parts
        value = int(value.strip(),10)
        if unit == 'kB':
          value = value * 1024 #(bytes)
          # value = value*1024
        memoryinfo[property] = value
  return memoryinfo

def main():
  log = logging.getLogger(__name__)
  out_hdlr = logging.StreamHandler(sys.stdout)
  out_hdlr.setFormatter(logging.Formatter(' %(message)s'))
  out_hdlr.setLevel(logging.INFO)
  log.addHandler(out_hdlr)
  log.setLevel(logging.INFO)
  parser = optparse.OptionParser()
  memory = 0
  cores = 0
  disks = {}
  hbaseEnabled = True
  # parser.add_option('-c', '--cores', default = 16,
  #                    help = 'Number of cores on each host')
  # parser.add_option('-m', '--memory', default = 64,
  #                   help = 'Amount of Memory on each host in GB')
  # parser.add_option('-d', '--disks', default = 4,
  #                   help = 'Number of disks on each host')
  parser.add_option('-k', '--hbase', default = "True",
                    help = 'True if HBase is installed, False is not')
  (options, args) = parser.parse_args()
  #discover disk info
  disks = discover_disks()
  cores = discover_cores()
  memory = discover_memory()['MemTotal'] / 1024 / 1024 / 1024
  if len(disks) == 0 :
      disks = 1

  # overrides discovered values
  # if options.disks is not None:
  #   disks = int (options.disks)
  # if options.cores is not None:
  #   cores = int (options.cores)
  # if options.memory is not None:
  #   memory = int (options.memory)
  hbaseEnabled = ast.literal_eval(options.hbase)

  log.info("Using cores=" +  str(len(cores)) + " memory=" + str(memory) + "GB" +
            " disks=" + str(disks) + " hbase=" + str(hbaseEnabled))


  minContainerSize = getMinContainerSize(memory)
  reservedStackMemory = getReservedStackMemory(memory)
  reservedHBaseMemory = 0
  if (hbaseEnabled):
    reservedHBaseMemory = getReservedHBaseMem(memory)
  reservedMem = reservedStackMemory + reservedHBaseMemory
  usableMem = memory - reservedMem
  memory -= (reservedMem)
  if (memory < 2):
    memory = 2
    reservedMem = max(0, memory - reservedMem)

  memory *= GB

  containers = int (min(2 * cores,
                         min(math.ceil(1.8 * float(disks)),
                              memory/minContainerSize)))
  if (containers <= 2):
    containers = 3

  log.info("Profile: cores=" + str(len(cores)) + " memory=" + str(memory) + "MB"
           + " reserved=" + str(reservedMem) + "GB" + " usableMem="
           + str(usableMem) + "GB" + " disks=" + str(disks))

  container_ram =  abs(memory/containers)
  if (container_ram > GB):
    container_ram = int(math.floor(container_ram / 512)) * 512
  log.info("Num Container=" + str(containers))
  log.info("Container Ram=" + str(container_ram) + "MB")
  log.info("Used Ram=" + str(int (containers*container_ram/float(GB))) + "GB")
  log.info("Unused Ram=" + str(reservedMem) + "GB")
  log.info("yarn.scheduler.minimum-allocation-mb=" + str(container_ram))
  log.info("yarn.scheduler.maximum-allocation-mb=" + str(containers*container_ram))
  log.info("yarn.nodemanager.resource.memory-mb=" + str(containers*container_ram))
  map_memory = container_ram
  reduce_memory = 2*container_ram if (container_ram <= 2048) else container_ram
  am_memory = max(map_memory, reduce_memory)
  log.info("mapreduce.map.memory.mb=" + str(map_memory))
  log.info("mapreduce.map.java.opts=-Xmx" + str(int(0.8 * map_memory)) +"m")
  log.info("mapreduce.reduce.memory.mb=" + str(reduce_memory))
  log.info("mapreduce.reduce.java.opts=-Xmx" + str(int(0.8 * reduce_memory)) + "m")
  log.info("yarn.app.mapreduce.am.resource.mb=" + str(am_memory))
  log.info("yarn.app.mapreduce.am.command-opts=-Xmx" + str(int(0.8*am_memory)) + "m")
  log.info("mapreduce.task.io.sort.mb=" + str(int(0.4 * map_memory)))
  pass

if __name__ == '__main__':
  try:
    main()
  except(KeyboardInterrupt, EOFError):
    print("\nAborting ... Keyboard Interrupt.")
    sys.exit(1)
