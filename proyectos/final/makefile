all:src/Main.class

src/Main.class: src/Main.java
	javac src/*.java

clean:
	$(RM) src/*.class Main.jar

run:
	java -cp src Main  src/DAT_ASCII_EURUSD_M1_2017_2019.csv
