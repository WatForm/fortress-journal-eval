# this Makefile is run with java directory

# after this the following works from the fortress-evaluation directory
# java -cp "java/libs/*" -Djava.library.path="java/libs"  countsorts.Countsorts
# java -cp "java/libs/*" -Djava.library.path="java/libs"  runfortress.Runfortress

# now that mvn download is working, we don't need to keep the commons-cli lib
# LIBS = $(filter-out libs/commons-cli-1.4.jar, $(wildcard libs/*))
LIBS = $(wildcard libs/*)

all: installfortress countsorts

countsorts: libs/countsorts.jar

libs/countsorts.jar:	Countsorts.java installfortress
	javac -d . -cp "libs/*:libs/fortressdebug-0.1.0/lib/*" Countsorts.java
	jar cfe countsorts.jar countsorts.Countsorts countsorts
	mv countsorts.jar libs/

installfortress: clean 
	./install_fortress.sh
	mvn org.apache.maven.plugins:maven-dependency-plugin:RELEASE:copy -Dartifact=commons-cli:commons-cli:1.4:jar -DoutputDirectory=libs


clean:
	rm -rf $(LIBS) countsorts runfortress

# Notes:



# jar cfe countsorts.jar countsorts.Countsorts countsorts
# creates the jar from all files in the directory
# f means create countsorts.jar
# c means create
# e means the entry point is countsorts.Countsorts (like the main class in a Manifest) 
# (e must be the last option)

# to run a jar, you can use -jar ..., but it ignores the -cp option
# -cp expects a list of jars; can use * in double quotes, but not "*.jar"
# if jar file you want to run is not with other libs, can do -cp "xx.jar:libs/*"

# jar tf countsorts.jar
# lists the files in the jar

# unzip -p countsorts.jar META-INF/MANIFEST.MF
# views the contents of the manifest

# javac -d . is used to create a package; along with "package" name at the top of the file
# the name of the files to put in the package is at the end
# -d . means puts the classes in a directory for this folder
