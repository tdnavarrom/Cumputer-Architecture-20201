
import java.util.ArrayList;

public class Results {
	float[][] results = new float[2][4];
	public synchronized void update(int row, int col, float value) {
		if(row == 0){
			if(results[row][col] < value) this.results[row][col] = value;
		}else if(row == 1 && value != 0){
			if(results[row][col]==0) this.results[row][col] = value;
			else if(results[row][col] > value) this.results[row][col] = value;
		}
	}

	public float[][] getResults(){
		return results;
	}

}
