import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.lang.Exception;
import java.util.ArrayList;
import java.util.List;

public class Knn {
    static int[][] readData(String filePath) throws IOException {
        final List<List<Integer>> images = new ArrayList<List<Integer>>();

        BufferedReader reader = null;
        try {
            reader = new BufferedReader(new FileReader(filePath));
            String line = reader.readLine();//skip header
            while ((line = reader.readLine()) != null) {
                final List<Integer> image = new ArrayList<Integer>();
                for (final String num : line.split(",")) {
                    image.add(Integer.parseInt(num, 10));
                }
                images.add(image);
            }
        } finally {
            if (reader != null) {
                reader.close();
            }
        }

        final int height = images.size();
        final int width = images.get(0).size();
        int[][] arr = new int[height][width];
        int i = 0;
        for (final List<Integer> image : images) {
            int j = 0;
            for (final int pixel : image) {
                arr[i][j++] = pixel;
            }
            i++;
        }
        return arr;

    }

    public static void main(String[] args) throws Exception  {
        final int[][] train_sample = readData("trainingsample.csv");
        final int[][] input_sample = readData("validationsample.csv");

        final long t = System.currentTimeMillis();
        int goodCount = 0;
        for (final int[] unknown : input_sample) {
            int[] match = null;
            int minDistance = Integer.MAX_VALUE;
            for (final int[] known : train_sample) {
                int distance = 0;
                for (int i = 1; i < known.length; i++) {//first column is label.
                    final int d = unknown[i]-known[i];
                    distance += (d*d);
                }

                if (distance < minDistance) {
                    minDistance = distance;
                    match = known;
                }
            }

            if (match[0] == unknown[0]) {
                goodCount++;
            }
        }

        System.out.format("%.1f%% Took: %.4f secs\n", goodCount*100.0/input_sample.length, (System.currentTimeMillis() - t)/1000.0);
    }
}
