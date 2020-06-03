
import java.io.IOException;
import java.util.List;
import java.util.Scanner;

public class Main {

	public static void findMaxMins(int row, int col, float val) {

		if(row == 0) {
			System.out.print("Max ");
		}else {
			System.out.print("Min ");
		}

		if(col == 0) {
			System.out.println("Apertura: " + val);
		}else if(col == 1) {
			System.out.println("Maximo: " + val);
		}else if(col == 2) {
			System.out.println("Bajo: " + val);
		}else {
			System.out.println("Cierre: " + val);
		}

	}

	public static void printResult(float[][] result) {

		for(int i = 0; i < result.length; i++) {
			for(int j = 0; j < result[0].length; j++) {
				findMaxMins(i,j,result[i][j]);
			}
		}

	}

	public static void main(String[] args) throws InterruptedException {

		String filename = args[0];
		Results results = new Results();
		Reader readFile = new Reader(filename);

		int contador = readFile.countNumLines();
		System.out.println("Press 1 to run secuential, press 2 to run directly with threads, press 3 to run with master thread and slave threads, press 4 to use optimized threads: ");
		Scanner in = new Scanner(System.in);
	    int option = in.nextInt();

	    long ini;

	    if (option == 1) {

			ini = System.currentTimeMillis();
			float[][] resultVals = readFile.readFileMain();
			ini = System.currentTimeMillis() - ini;

			System.out.println("Time: " + ini);
			printResult(resultVals);

		} else if (option == 2) {

			int num_hilos = 20;
			int particiones = contador / num_hilos;
			int restantes = 0;

			ini = System.currentTimeMillis();
			Slave[] slaves = new Slave[num_hilos];
			for(int i = 0; i < num_hilos; i++) {

				if(i == num_hilos-1) restantes = contador % num_hilos;

				Slave slave = new Slave(i, particiones, readFile, results, restantes);
				slaves[i] = slave;
				//slave.setPriority(Thread.MAX_PRIORITY);
				slave.start();
			}

			for(int i = 0; i<slaves.length;++i){
				if(slaves[i].isAlive()){
					slaves[i].join();
				}
			}
			ini = System.currentTimeMillis() - ini;

			System.out.println("Time: " + ini);
			printResult(readFile.getResult());

		} else if (option == 3) {
			ini = System.currentTimeMillis();
			int num_hilos = 20;

			Master master = new Master(readFile, results, num_hilos);
			master.start();
			master.join();
			ini = System.currentTimeMillis() - ini;

			System.out.println("Time: " + ini);
			printResult(results.getResults());

		} else if(option == 4) {
			ini = System.currentTimeMillis();

			int cores = Runtime.getRuntime().availableProcessors();

			int num_hilos = cores;
			Master master = new Master(readFile, results,  num_hilos);
			master.start();
			master.join();
			ini = System.currentTimeMillis() - ini;

			System.out.println("Time: " + ini);
			printResult(results.getResults());
		}
	}
}
