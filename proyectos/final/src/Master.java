import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;


public class Master extends Thread {

    private Reader readfile;
    private  Results results;
    private int num_hilos = 0;
    private int contador=0;

    public Master(Reader readfile,Results results, int num_hilos) {
        this.readfile = readfile;
        this.results = results;
        this.num_hilos = num_hilos;
    }

    public void run(){

        readfile.readFileMaster();
        int contador = readfile.getContador();
        int particiones = contador/num_hilos;
        int restantes = 0;

        float[][] data = readfile.getDataMaster();

        float[][] temp_data = new float[particiones][4];

        Minions minions;
        Minions[] arrMinions = new Minions[num_hilos];

        for (int i = 0; i < num_hilos; ++i) {

            temp_data = new float[particiones][4];

            int temp_end_of_range = (i + 1) * particiones;

            if(i == num_hilos-1) restantes = contador % num_hilos;

            if(restantes != 0) {
                temp_end_of_range = ((i + 1) * particiones) + restantes;
                temp_data = new float[particiones+restantes][4];
            }
            //else Thread.currentThread().setPriority(Thread.MAX_PRIORITY);
            int start = i * particiones;

            temp_data = Arrays.copyOfRange(data,start,temp_end_of_range).clone();

            /*for(int j = start; j<temp_end_of_range;j++) {
                temp_data[j - start] = data[j].clone();
            }*/
            //System.out.println(temp_data.length);

            minions = new Minions(results,temp_data);
            arrMinions[i] = minions;
            minions.start();

        }
        try{
            for(int i = 0; i<arrMinions.length;++i){
                if(arrMinions[i].isAlive()){
                    arrMinions[i].join();
                }
            }
        }
        catch (Exception e){

        }
    }
}