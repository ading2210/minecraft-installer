#!/usr/bin/python3

import getpass, os, platform, subprocess, sys
from urllib.parse import urlparse

user = getpass.getuser()
homeDir = "/home/"+user+"/"
mcDir = homeDir[:-1]+"/minecraft/"
arch = platform.machine()
args = sys.argv

if arch == "armv7l":
  bits = 32
else:
  bits = 64

links = {
  "launcher": "https://launcher.mojang.com/v1/objects/eabbff5ff8e21250e33670924a0c5e38f47c840b/launcher.jar",
  "jdk8_32": "https://www.dropbox.com/s/ea5aihehqvvzxhb/jdk-8u251-linux-arm32.gz",
  "jdk8_64": "https://www.dropbox.com/s/9tsv6o8qzgd0fxf/jdk-8u251-linux-arm64.gz",
  "lwjgl3_32": "https://www.dropbox.com/s/6n4ouhb69abxkqx/lwjgl3arm32.tar.gz",
  "lwjgl3_64": "https://www.dropbox.com/s/ks8adxlk7r61v1o/lwjgl3arm64.tar.gz",
  "optifine_1.16.3": "https://www.dropbox.com/s/p6shx9qy1i20gh6/OptiFine_1.16.3_HD_U_G5.jar"
  }

def run(command):
  subprocess.call(command, shell=True)

def getFilename(link):
  parse = urlparse(link)
  filename = os.path.basename(parse.path)
  return filename

def download(link):
  filename = mcDir+getFilename(link)
  run("wget {url} -O {file} -q --show-progress".format(url=link, file=filename))

def fileExists(filename):
  return os.path.exists(filename)

def editProfiles(name, version):
  if fileExists(homeDir+".minecraft/launcher_profiles.json") == False:
    run("mkdir ~/.minecraft")
    file = open(homeDir+".minecraft/launcher_profiles.json","w")
    file.write(str({"profiles":{}}))
    file.close()
  file = open(homeDir+".minecraft/launcher_profiles.json")
  json = eval(file.read())
  file.close()
  json["profiles"][name] = {"name": name, "lastVersionId":version}
  json["selectedProfile"] = name
  file = open(homeDir+".minecraft/launcher_profiles.json", "w")
  file.write(str(json))
  file.close

print("System architecture: "+str(bits)+" bit "+arch)

print("Creating folders...")
if fileExists(mcDir) == False:
  run("mkdir ~/minecraft")

print("Downloading launcher...")
if fileExists(mcDir+"launcher.jar") == False:
  download(links["launcher"])

print("Downloading Java...")
if fileExists(mcDir+"jdk8") == False:
  if bits == 32:
    download(links["jdk8_32"])
  else:
    download(links["jdk8_64"])

print("Downloading lwjgl3...")
if fileExists(mcDir+"lwjgl3") == False:
  if bits == 32:
    download(links["lwjgl3_32"])
  else:
    download(links["lwjgl3_64"])

print("Downloading Optifine...")
if fileExists(mcDir+getFilename(links["optifine_1.16.3"])) == False:
  download(links["optifine_1.16.3"])

print("Downloads complete.")

print("Extracting Java...")
if fileExists("{mcDir}jdk8".format(mcDir=mcDir)) == False:
  if bits == 32:
    filename = mcDir+getFilename(links["jdk8_32"])
  else:
    filename = mcDir+getFilename(links["jdk8_32"])
  run("tar -zxf {filename} -C {mcDir}".format(filename=filename,mcDir=mcDir))
  #run("mkdir {mcDir}jdk8".format(mcDir=mcDir))
  run("mv {mcDir}jdk1.8.0_251 {mcDir}jdk8".format(mcDir=mcDir))

print("Extracting lwjgl3...")
if fileExists("{mcDir}lwjgl3".format(mcDir=mcDir)) == False:
  run("mkdir {mcDir}lwjgl3".format(mcDir=mcDir))
  if bits == 32:
    filename = mcDir+getFilename(links["lwjgl3_32"])
  else:
    filename = mcDir+getFilename(links["lwjgl3_64"])
  run("tar -zxf {filename} -C {mcDir}lwjgl3".format(filename=filename,mcDir=mcDir))

print("Extracting complete.")

print("Preparing launcher...")
editProfiles("1.16.3","1.16.3")

print("Opening launcher...")
print("Please login, click play, and when the launcher reopens, close it.")
run("{mcDir}/jdk8/bin/java -jar {mcDir}/launcher.jar >/dev/null".format(mcDir=mcDir))

print("Opening Optifine installer...")
print("Please click install, wait, then close the installer once done.")
run("{mcDir}/jdk8/bin/java -jar {mcDir}/OptiFine_1.16.3_HD_U_G5.jar >/dev/null".format(mcDir=mcDir))

print("Opening launcher...")
print("Please login, click play, and when the launcher reopens, close it.")
run("{mcDir}/jdk8/bin/java -jar {mcDir}/launcher.jar >/dev/null".format(mcDir=mcDir))

print("Installation complete.")





