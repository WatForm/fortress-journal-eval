import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

import java.io.*;

public class FOF2AlloyParser {

    public static String parse(String filePath) throws IOException {
        InputStream inputStream = new FileInputStream(filePath);
        CharStream stream = CharStreams.fromStream(inputStream);
        FOFTPTPLexer lexer = new FOFTPTPLexer(stream);
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        FOFTPTPParser parser = new FOFTPTPParser(tokens);
        ParseTree tree = parser.spec();
        if (parser.getNumberOfSyntaxErrors() >= 1)
            return "SyntaxError";
        FOF2Alloy converter = new FOF2Alloy(filePath);
        String facts = converter.visit(tree);
        // Append declarations at the front
        return converter.declarationString() + facts;
    }
}
