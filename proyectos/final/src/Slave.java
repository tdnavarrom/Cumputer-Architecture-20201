
import java.util.List;

public class Slave extends Thread{
	private int temp_cont, particiones;
	private Reader readFile;
	private Results results;
	private int restantes;

	public Slave(int temp_cont, int particiones, Reader readFile, Results results, int restantes) {
		this.temp_cont = temp_cont;
		this.particiones = particiones;
		this.readFile = readFile;
		this.results = results;
		this.restantes = restantes;
	}

	public void run() {

		//System.out.println("Thread "+Thread.currentThread().getId()+" starting");
		int temp_end_of_range = (temp_cont + 1) * particiones;


		if(restantes != 0) temp_end_of_range = ((temp_cont + 1) * particiones) + restantes;
		else Thread.currentThread().setPriority(Thread.MAX_PRIORITY);
		readFile.readFileSlaves(temp_cont * particiones, temp_end_of_range); // begin , end of thread

		//System.out.println ("Thread " + Thread.currentThread().getId() + " is finished");
	}

}
