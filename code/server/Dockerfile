FROM python:3.7-alpine
# I would like to introduce something new, the 'WORKDIR' command.
# This command changes the base directory of your image.
# Here we define '/server/' as base directory (where all commands will be executed).
WORKDIR /home/clement/WKS/AALTO/BigData/assignment-2-784795/code/server/
# In order to launch our python code, we must import the 'server.py' and 'index.html' file.
# We use the keyword 'ADD' to do that.
# Just a remember, the first parameter 'server.py' is the name of the file on the host.
# The second parameter '/server/' is the path where to put the file on the image.
# Here we put files at the image '/server/' folder.
#ADD server.py /home/clement/WKS/AALTO/BigData/assignment-2-784795/code/server/
#COPY requirements.txt requirements.txt
#RUN pip install -r requirements.txt
COPY . .
