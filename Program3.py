import boto3
import os
import sys
from os import walk

# Prints command line arguments
#print(sys.argv)

if(sys.argv.__len__() != 4):
    print("python .\Program3.py {Backup} {directoryName} {bucketName}")
    print("python .\Program3.py {Restore} {bucketName} {directoryName}")
    sys.exit(0)

# Backup or Restore
command = sys.argv[1]

#Checks to see if user is backing up to bucket or restoring from bucket
if(command == "Backup"):
    directoryName = sys.argv[2]
    bucketName = sys.argv[3]

if(command == "Restore"):
    bucketName = sys.argv[2]
    directoryName = sys.argv[3]

if(command != "Backup" and command != "Restore"):
    print("python .\Program3.py {Backup} {directoryName} {bucketName}")
    print("python .\Program3.py {Restore} {bucketName} {directoryName}")
    sys.exit(0)

print(directoryName + " " + bucketName)

files = []

# Shows all current buckets
s3 = boto3.resource('s3')
buckets = s3.buckets.all()
for bucket in buckets:
    print(bucket.name)

# Creating a new bucket to backup files
print("Creating Bucket: ", bucketName, " in us-west-1") # may need to change us-west-1 to general region if possible or specified region
s3.create_bucket(Bucket=bucketName, CreateBucketConfiguration={'LocationConstraint': 'us-west-1'})

#Traverse through all of the directories
for (dirpath, dirnames, fileNames) in walk(directoryName):
    print("dirpath: ", dirpath) # prints the current directory path
    addedFiles = []
    print("Files: ", fileNames)
    folderName = dirpath[directoryName.__len__():]

    if(dirpath[dirpath.__len__() - 1] != '\\'):
        dirpath += '\\'
    
    #Uploads file to recently create bucket
    for fileName in fileNames:
        print("File to add: ", fileName)
        print("Path to file: ", dirpath)
        print(dirpath + fileName)
        s3.Object(bucketName, fileName).put(Body=open(dirpath + fileName, "rb"))
        #s3.meta.client.upload_file(fileName, bucketName, folderName)
        addedFiles.extend(fileName)

#     print("Done with this directory, adding it to fileNames list as completed")
#     files.extend(fileNames)
    
# print(files)
# if(files.__len__() == 0):
#     print("Invalid directory or no items found in directory")

# s3.Object(bucketName, fileName).put(Body=open(fullPath + fileName, "rb"))

# #Prints out all buckets and their items
# for bucket in s3.buckets.all():
#     print("Bucket: ", bucket.name)
#     print("---------------")
#     for key in bucket.objects.all():
#         print(key.key)
#     print(" ")