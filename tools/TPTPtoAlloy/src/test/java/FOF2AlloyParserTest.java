import org.junit.jupiter.api.Test;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class FOF2AlloyParserTest {

    @Test
    public void test_function() throws IOException {
        String tptp_content = "fof('defined-prop',axiom,( " +
                "  h(j(a20)) = a20\n" +
                "& h(j(a21)) = a21\n" +
                "& h(j(a22)) = a22\n" +
                "& h(j(a23)) = a23\n" +
                "& h(j(a24)) = a24\n" +
                "& j(h(a10)) = a10\n" +
                "& j(h(a11)) = a11\n" +
                "& j(h(a12)) = a12\n" +
                "& j(h(a13)) = a13\n" +
                "& j(h(a14)) = a14\n" +
                ")).";
        
        File file = File.createTempFile( "test", "p");
        file.deleteOnExit();
        FileWriter fw = new FileWriter(file);
        fw.write(tptp_content);
        fw.flush();

        String result = FOF2AlloyParser.parse(file.getPath());
        String expected = "sig _UNIV{\n" +
                "    j_ : one _UNIV,\n" +
                "    h_ : one _UNIV\n" +
                "}\n" +
                "one sig a10_, a11_, a12_, a13_, a14_, a20_, a21_, a22_, a23_, a24_ in _UNIV{}\n\n\n" +
                "fact{\n" +
                "    (((((((((((h_[j_[a20_]] = a20_) and (h_[j_[a21_]] = a21_)) and (h_[j_[a22_]] = a22_)) and (h_[j_[a23_]] = a23_)) and (h_[j_[a24_]] = a24_)) and (j_[h_[a10_]] = a10_)) and (j_[h_[a11_]] = a11_)) and (j_[h_[a12_]] = a12_)) and (j_[h_[a13_]] = a13_)) and (j_[h_[a14_]] = a14_)))\n\n" +
                "}\n";
        assertEquals(expected, result);
    }

    @Test
    public void test_proposition() throws IOException {
        String tptp_content = "fof(exists,axiom,(\n" +
                "    ! [X,Y] :\n" +
                "      ( exists(X)\n" +
                "    <=> ( existsIn(X,X)\n" +
                "        | ( existsIn(X,Y)\n" +
                "          & X != Y ) ) ) )).";
        File file = File.createTempFile( "test", "p");
        file.deleteOnExit();
        FileWriter fw = new FileWriter(file);
        fw.write(tptp_content);
        fw.flush();

        String result = FOF2AlloyParser.parse(file.getPath());
        String expected = "sig _UNIV{\n" +
                "    existsIn_ : set _UNIV\n" +
                "}\n" +
                "sig exists_ in _UNIV{}\n\n" +
                "fact{\n" +
                "    ((all X_, Y_: _UNIV | ((((X_) in exists_) iff ((((X_ -> X_) in existsIn_) or ((((X_ -> Y_) in existsIn_) and (not (X_ = Y_))))))))))\n\n" +
                "}\n";
        assertEquals(expected, result);
    }


    @Test
    public void test_file_import() throws IOException {
        String tptp_content = "include('Axioms/axiom.ax').\n" +
                "fof('defined-prop',axiom,( " +
                "( a = b => $true ) & " +
                "( $false  => a = b))" +
                ").";
        File tmpdir = Files.createTempDirectory("tmpDir").toFile();
        File file = new File(tmpdir.getPath()+ "/Problems/TEST/test.p");
        file.getParentFile().mkdirs();
        file.deleteOnExit();
        FileWriter fw = new FileWriter(file);
        fw.write(tptp_content);
        fw.flush();

        String tptp_content2 = "fof('defined-prop2',axiom,( " +
                "( b = c => $true ) & " +
                "( $false  => b = c))" +
                ").";
        File file2 = new File(tmpdir.getPath()+ "/Axioms/axiom.ax");
        file2.getParentFile().mkdirs();
        file2.deleteOnExit();
        fw = new FileWriter(file2);
        fw.write(tptp_content2);
        fw.flush();

        String result = FOF2AlloyParser.parse(file.getPath());
        String expected = "sig _UNIV{\n\n}\n" +
                "one sig a_, b_, c_ in _UNIV{}\n\n\n" +
                "pred true {}\n" +
                "pred false { not true }\n\n" +
                "fact{\n" +
                "    (((((b_ = c_) implies true)) and ((false implies (b_ = c_)))))\n\n" +
                "}\n\n" +
                "fact{\n" +
                "    (((((a_ = b_) implies true)) and ((false implies (a_ = b_)))))\n" +
                "\n}\n";
        assertEquals(expected, result);
    }

    @Test
    public void test_defined_proposition() throws IOException {
        String tptp_content = "fof('defined-prop',axiom,( " +
                "( a = b => $true ) & " +
                "( $false  => a = b))" +
                ").";
        File file = File.createTempFile( "test", "p");
        file.deleteOnExit();
        FileWriter fw = new FileWriter(file);
        fw.write(tptp_content);
        fw.flush();

        String result = FOF2AlloyParser.parse(file.getPath());
        String expected = "sig _UNIV{\n\n}\n" +
                "one sig a_, b_ in _UNIV{}\n\n\n" +
                "pred true {}\n" +
                "pred false { not true }\n\n" +
                "fact{\n" +
                "    (((((a_ = b_) implies true)) and ((false implies (a_ = b_)))))\n\n" +
                "}\n";
        assertEquals(expected, result);
    }
}


