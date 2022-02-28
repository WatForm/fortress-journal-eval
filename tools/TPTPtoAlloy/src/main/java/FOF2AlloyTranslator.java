import java.io.IOException;


public class FOF2AlloyTranslator {
    public static void main(String[] args) {
        try {
            FOF2AlloyParser parser = new FOF2AlloyParser();
            String result = parser.parse(args[0]);
            System.out.println(result);
            if(args.length > 1){
                System.out.println("run {} for exactly " + args[1] + " _UNIV\n");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
