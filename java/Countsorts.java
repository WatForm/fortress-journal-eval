package countsorts;

import fortress.msfol.*;
import fortress.msfol.Term.*;
import fortress.msfol.Sort.*;
import fortress.msfol.FuncDecl.*;
import fortress.inputs.*;
import fortress.modelfind.*;
import fortress.operations.TheoryOps;
import fortress.util.Errors;

import java.util.*;
import java.io.*;
import scala.util.Either;

import org.apache.commons.cli.*;

public class Countsorts {

    public static void main(String[] args) throws Exception {

        Options options = new Options();

        Option input = new Option("f", "input", true, "input file path");
        input.setRequired(true);
        options.addOption(input);

        CommandLineParser cmdlineparser = new GnuParser();
        HelpFormatter formatter = new HelpFormatter();
        CommandLine cmd;

        cmd = null;
        try {
            cmd = cmdlineparser.parse(options, args);
        } catch (ParseException e) {
            System.out.println(e.getMessage());
            formatter.printHelp("countsorts", options);
            System.exit(1);
        }

        String inputFilePath = cmd.getOptionValue("input");

		FileInputStream fileStream = null;
        try {
	        fileStream = new FileInputStream(inputFilePath);
	    } catch (FileNotFoundException e) {
	    	System.out.println(inputFilePath+" not found.");
	    	System.exit(1);
        }
        Either<Errors.ParserError,Theory> result;
	    if (inputFilePath.toLowerCase().endsWith(".smt2") || inputFilePath.toLowerCase().endsWith(".smt")) {
            SmtLibParser parser = new SmtLibParser();
            result = parser.parse(fileStream);
        } else if (inputFilePath.toLowerCase().endsWith(".p")) {
            TptpFofParser parser = new TptpFofParser();
            result = parser.parse(inputFilePath);
        } else {
        	System.out.println("Cannot parse: "+ inputFilePath);
            System.exit(1);
            return;
        }
        if (result.isLeft()) {
            System.out.println("Cannot parse: "+ inputFilePath);
            System.exit(1);
        }
        Theory thy = result.right().getOrElse(null);

        try (ModelFinder modelfinder = ModelFinder.createDefault()) {
            TheoryOps theoryops = TheoryOps.wrapTheory(fortress.transformers.TypecheckSanitizeTransformer.apply(thy));
            modelfinder.setTheory(thy);
            System.out.println(theoryops.sortCount()+", "+theoryops.inferSortsCount());
        }
    	System.exit(0);
    }
}