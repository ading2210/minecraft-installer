#!/usr/bin/python3

import getpass, os, platform, subprocess, requests, sys

#ACCOUNT INFO:
#You must fill this out for this launcher to work.
#For unmigrated accouts, put your username in the login field.
username = "Steve"
login = "example@example.com"
password = "password123"

#CONFIGURATION:
#Edit this if you want this to work on other MC versions

gameVersion = "1.16.3"
gameVersionShort = "1.16"
optifineVersion = "HD_U_G5"
cp = "{homeDir}.minecraft/libraries/optifine/OptiFine/{version}_{optifineVersion}/OptiFine-{version}_{optifineVersion}.jar:{homeDir}.minecraft/libraries/optifine/launchwrapper-of/2.2/launchwrapper-of-2.2.jar:{homeDir}.minecraft/libraries/com/mojang/patchy/1.1/patchy-1.1.jar:{homeDir}.minecraft/libraries/oshi-project/oshi-core/1.1/oshi-core-1.1.jar:{homeDir}.minecraft/libraries/net/java/dev/jna/jna/4.4.0/jna-4.4.0.jar:{homeDir}.minecraft/libraries/net/java/dev/jna/platform/3.4.0/platform-3.4.0.jar:{homeDir}.minecraft/libraries/com/ibm/icu/icu4j/66.1/icu4j-66.1.jar:{homeDir}.minecraft/libraries/com/mojang/javabridge/1.0.22/javabridge-1.0.22.jar:{homeDir}.minecraft/libraries/net/sf/jopt-simple/jopt-simple/5.0.3/jopt-simple-5.0.3.jar:{homeDir}.minecraft/libraries/io/netty/netty-all/4.1.25.Final/netty-all-4.1.25.Final.jar:{homeDir}.minecraft/libraries/com/google/guava/guava/21.0/guava-21.0.jar:{homeDir}.minecraft/libraries/org/apache/commons/commons-lang3/3.5/commons-lang3-3.5.jar:{homeDir}.minecraft/libraries/commons-io/commons-io/2.5/commons-io-2.5.jar:{homeDir}.minecraft/libraries/commons-codec/commons-codec/1.10/commons-codec-1.10.jar:{homeDir}.minecraft/libraries/net/java/jinput/jinput/2.0.5/jinput-2.0.5.jar:{homeDir}.minecraft/libraries/net/java/jutils/jutils/1.0.0/jutils-1.0.0.jar:{homeDir}.minecraft/libraries/com/mojang/brigadier/1.0.17/brigadier-1.0.17.jar:{homeDir}.minecraft/libraries/com/mojang/datafixerupper/4.0.26/datafixerupper-4.0.26.jar:{homeDir}.minecraft/libraries/com/google/code/gson/gson/2.8.0/gson-2.8.0.jar:{homeDir}.minecraft/libraries/com/mojang/authlib/1.6.25/authlib-1.6.25.jar:{homeDir}.minecraft/libraries/org/apache/commons/commons-compress/1.8.1/commons-compress-1.8.1.jar:{homeDir}.minecraft/libraries/org/apache/httpcomponents/httpclient/4.3.3/httpclient-4.3.3.jar:{homeDir}.minecraft/libraries/commons-logging/commons-logging/1.1.3/commons-logging-1.1.3.jar:{homeDir}.minecraft/libraries/org/apache/httpcomponents/httpcore/4.3.2/httpcore-4.3.2.jar:{homeDir}.minecraft/libraries/it/unimi/dsi/fastutil/8.2.1/fastutil-8.2.1.jar:{homeDir}.minecraft/libraries/org/apache/logging/log4j/log4j-api/2.8.1/log4j-api-2.8.1.jar:{homeDir}.minecraft/libraries/org/apache/logging/log4j/log4j-core/2.8.1/log4j-core-2.8.1.jar:{homeDir}.minecraft/libraries/org/lwjgl/lwjgl/3.2.2/lwjgl-3.2.2.jar:{homeDir}.minecraft/libraries/org/lwjgl/lwjgl-jemalloc/3.2.2/lwjgl-jemalloc-3.2.2.jar:{homeDir}.minecraft/libraries/org/lwjgl/lwjgl-openal/3.2.2/lwjgl-openal-3.2.2.jar:{homeDir}.minecraft/libraries/org/lwjgl/lwjgl-opengl/3.2.2/lwjgl-opengl-3.2.2.jar:{homeDir}.minecraft/libraries/org/lwjgl/lwjgl-glfw/3.2.2/lwjgl-glfw-3.2.2.jar:{homeDir}.minecraft/libraries/org/lwjgl/lwjgl-stb/3.2.2/lwjgl-stb-3.2.2.jar:{homeDir}.minecraft/libraries/org/lwjgl/lwjgl-tinyfd/3.2.2/lwjgl-tinyfd-3.2.2.jar:{homeDir}.minecraft/libraries/com/mojang/text2speech/1.11.3/text2speech-1.11.3.jar:{homeDir}.minecraft/versions/{version}-OptiFine_{optifineVersion}/{version}-OptiFine_{optifineVersion}.jar"
maxRam = "1G"

#LAUNCHER CODE:
#You shouldn't need to edit past this

def run(command):
  subprocess.call(command, shell=True)

user = getpass.getuser()
homeDir = "/home/"+user+"/"
mcDir = homeDir+"/minecraft/"
arch = platform.machine()
cp = cp.format(homeDir=homeDir, version=gameVersion, optifineVersion=optifineVersion)

print("Logging into Mojang account...")

loginData = {"username":login,
             "password":password,
             "agent":{
               "name": "Minecraft",
               "version": 1
               }
             }
auth = requests.post("https://authserver.mojang.com/authenticate", json=loginData)
json = auth.json()
try:
  token = json["accessToken"]
  uuid = str(json["selectedProfile"]["id"])
except:
  print(json["errorMessage"])
  sys.exit()
print("Launching game...")

run("""{mcDir}/jdk8/bin/java -Xmx{ram}
-XX:+UseConcMarkSweepGC -XX:+CMSIncrementalMode -XX:-UseAdaptiveSizePolicy
-Djava.library.path={mcDir}/lwjgl3 -Dorg.lwjgl.util.Debug=true
-Dminecraft.launcher.brand=java-minecraft-launcher
-Dminecraft.launcher.version=1.6.93
-cp {cp} net.minecraft.launchwrapper.Launch
--username {username}
--accessToken {token}
--uuid {uuid}
--version {version}
--userProperties {userProperties}
--gameDir ~/.minecraft
--assetsDir ~/.minecraft/assets
--assetIndex {version}
--tweakClass optifine.OptiFineTweaker"""
    .replace("\n"," ")
    .format(mcDir=mcDir, cp=cp, username=username, token=token, uuid=uuid,
            version=gameVersionShort,userProperties="{}",ram=maxRam))
