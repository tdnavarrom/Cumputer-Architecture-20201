
import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Reader {
	private String filename = null;
	private List<float[]> data = new ArrayList<>();
	private float[][] dataMaster;
	private int contador = 0;
	private float[][] results = new float[2][4];

	public Reader(String filename) {
		this.filename = filename;
		this.results[1][0] = Integer.MAX_VALUE;
		this.results[1][1] = Integer.MAX_VALUE;
		this.results[1][2] = Integer.MAX_VALUE;
		this.results[1][3] = Integer.MAX_VALUE;
	}

	public int countNumLines() {
		try (BufferedReader br = new BufferedReader(new FileReader(this.filename))) {
			String line;
			while ((line = br.readLine()) != null) {
				this.contador++;
			}
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		return this.contador;
	}

	public synchronized float[][] readFileSlaves(int start, int end) {

		try (BufferedReader br = new BufferedReader(new FileReader(this.filename))) {
			String line;
			String[] values;

			for (int i = 0; i < end; i++) {
				line = br.readLine();
				if (i >= start && i < end && line != null) {
					values = Arrays.copyOfRange(line.split(";"), 2, 6);
					results[0][0] = results[0][0] < Float.parseFloat(values[0])? Float.parseFloat(values[0]):results[0][0];
					results[0][1] = results[0][1] < Float.parseFloat(values[1])? Float.parseFloat(values[1]):results[0][1];
					results[0][2] = results[0][2] < Float.parseFloat(values[2])? Float.parseFloat(values[2]):results[0][2];
					results[0][3] = results[0][3] < Float.parseFloat(values[3])? Float.parseFloat(values[3]):results[0][3];
					results[1][0] = results[1][0] > Float.parseFloat(values[0])? Float.parseFloat(values[0]):results[1][0];
					results[1][1] = results[1][1] > Float.parseFloat(values[1])? Float.parseFloat(values[1]):results[1][1];
					results[1][2] = results[1][2] > Float.parseFloat(values[2])? Float.parseFloat(values[2]):results[1][2];
					results[1][3] = results[1][3] > Float.parseFloat(values[3])? Float.parseFloat(values[3]):results[1][3];
					//System.out.println(results[0][0]);
				}
			}
			br.close();

		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (Exception e) {
			System.out.println(e);
		}
		return results;
	}

	public float[][] readFileMain(){

		try (BufferedReader br = new BufferedReader(new FileReader(this.filename))) {
			String line;
			String[] values;
			while ((line = br.readLine()) != null) {
				values = line.split(";");

				values = Arrays.copyOfRange(values, 2, 6);
				results[0][0] = results[0][0] < Float.parseFloat(values[0])? Float.parseFloat(values[0]):results[0][0];
				results[0][1] = results[0][1] < Float.parseFloat(values[1])? Float.parseFloat(values[1]):results[0][1];
				results[0][2] = results[0][2] < Float.parseFloat(values[2])? Float.parseFloat(values[2]):results[0][2];
				results[0][3] = results[0][3] < Float.parseFloat(values[3])? Float.parseFloat(values[3]):results[0][3];
				results[1][0] = results[1][0] > Float.parseFloat(values[0])? Float.parseFloat(values[0]):results[1][0];
				results[1][1] = results[1][1] > Float.parseFloat(values[1])? Float.parseFloat(values[1]):results[1][1];
				results[1][2] = results[1][2] > Float.parseFloat(values[2])? Float.parseFloat(values[2]):results[1][2];
				results[1][3] = results[1][3] > Float.parseFloat(values[3])? Float.parseFloat(values[3]):results[1][3];

			}

		}catch(

				FileNotFoundException e)
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}catch(
				IOException e)
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}catch(
				Exception e)
		{
			System.out.println(e);
		}
		return results;
	}

	public void readFileMaster() {

		dataMaster = new float[this.contador][4];
		int count = 0;
		try (BufferedReader br = new BufferedReader(new FileReader(this.filename))) {
			String line;
			while ((line = br.readLine()) != null) {
				String[] values = line.split(";");
				for(int j =2; j < values.length-1; j++){
					dataMaster[count][j-2] = Float.parseFloat(values[j]);
				}

				//this.data.add(floatData);
				count++;
			}
			br.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		this.contador = count;
	}

	public List<float[]> getData() {
		return data;
	}

	public float[][] getDataMaster() {
		return dataMaster;
	}

	public float[][] getResult() {
		return this.results;
	}

	public int getContador() {
		return this.contador;
	}
}