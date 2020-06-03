import java.util.ArrayList;
import java.util.List;

public class Evaluator {

	float[][] mat;

	public Evaluator(float[][] mat) {
		this.mat = mat;
	}

	public float[][] ComparatorPrecio() {

		float[][] result = new float[2][4];

		result[0][0] = mat[0][0]; // max apertura
		result[1][0] = mat[0][0]; // min apertura

		result[0][1] = mat[0][1]; // max maximo
		result[1][1] = mat[0][1]; // min maximo

		result[0][2] = mat[0][2]; // max bajo
		result[1][2] = mat[0][2]; // min bajo

		result[0][3] = mat[0][3]; // max cierre
		result[1][3] = mat[0][3]; // min cierre

		for (float[] list : this.mat) {

			if (list[0] > result[0][0]) {
				result[0][0] = list[0];
			} else if (list[0] < result[1][0]) {
				result[1][0] = list[0];
			}
			if (list[1] > result[0][1]) {
				result[0][1] = list[1];
			} else if (list[1] < result[1][1]) {
				result[1][1] = list[1];
			}
			if (list[2] > result[0][2]) {
				result[0][2] = list[2];
			} else if (list[2] < result[1][2]) {
				result[1][2] = list[2];
			}
			if (list[3] > result[0][3]) {
				result[0][3] = list[3];
			} else if (list[3] < result[1][3]) {
				result[1][3] = list[3];
			}
		}

		return result;

	}

}