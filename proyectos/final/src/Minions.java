import java.util.List;

public class Minions extends Thread{
    
    private float[][] floatData;
	private Results results;

	public Minions(Results results,  float[][] floatData) {
		this.results = results;
		this.floatData = floatData;
	}

	public void run() {


		Evaluator evaluator = new Evaluator(floatData);

		float[][] temp_precios = evaluator.ComparatorPrecio();


		for (int j = 0; j < 4; j++) {
			results.update(0, j, temp_precios[0][j]);
			results.update(1, j, temp_precios[1][j]);
		}
		//System.out.println("Thread " + Thread.currentThread().getId() + " is finished");
	}
}