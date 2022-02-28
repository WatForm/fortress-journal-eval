/*
 * Copyright 2016 Amirhossein Vakili
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.CharStreams;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.tree.ParseTree;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.*;

/**
 * Created by Amirhossein Vakili.
 */
public class FOF2Alloy extends FOFTPTPBaseVisitor<String> {

    private Map<String, Integer> relSym, funSym;

    private Set<String> constants, props, sets;

    private Set<String> vars;

    public static final String univ = "_UNIV";

    private String filePath;

    private Boolean errorDuringImport = false;
    private Boolean builtinBoolean = false;

    public FOF2Alloy(String filePath) {
        relSym = new HashMap<>();
        funSym = new HashMap<>();
        constants = new TreeSet<>();
        props = new TreeSet<>();
        sets = new TreeSet<>();
        vars = new TreeSet<>();
        this.filePath = filePath;
    }

    public String declarationString() {
        StringBuilder declarations = new StringBuilder("sig _UNIV{\n");
        if (!relSym.isEmpty()) {
            Iterator<Map.Entry<String, Integer>> it = relSym.entrySet().iterator();
            Map.Entry<String, Integer> el = it.next();
            declarations.append("    " + el.getKey() + " : " + predDec(el.getValue()));
            while (it.hasNext()) {
                el = it.next();
                declarations.append(",\n    " + el.getKey() + " : " + predDec(el.getValue()));
            }
            for (Map.Entry<String, Integer> e : funSym.entrySet()) {
                declarations.append(",\n    " + e.getKey() + " : " + funDec(e.getValue()));
            }
        } else {
            if (!funSym.isEmpty()) {
                Iterator<Map.Entry<String, Integer>> it = funSym.entrySet().iterator();
                Map.Entry<String, Integer> el = it.next();
                declarations.append("    " + el.getKey() + " : " + funDec(el.getValue()));
                while (it.hasNext()) {
                    el = it.next();
                    declarations.append(",\n    " + el.getKey() + " : " + funDec(el.getValue()));
                }
            }
        }
        declarations.append("\n}\n");

        if (!constants.isEmpty()) {
            declarations.append("one sig ");
            Iterator<String> it = constants.iterator();
            declarations.append(it.next());
            while (it.hasNext())
                declarations.append(", " + it.next());
            declarations.append(" in _UNIV{}\n\n");
        }

        if (!sets.isEmpty()) {
            declarations.append("sig ");
            Iterator<String> it = sets.iterator();
            declarations.append(it.next());
            while (it.hasNext())
                declarations.append(", " + it.next());
            declarations.append(" in _UNIV{}\n");
        }
        declarations.append('\n');
        if (!props.isEmpty()) {
            declarations.append("one sig _BOOLEAN{}\nsig ");
            Iterator<String> it = props.iterator();
            declarations.append(it.next());
            while (it.hasNext())
                declarations.append(", " + it.next());
            declarations.append(" in _BOOLEAN{}\n\n");
        }
        if (errorDuringImport) return "SyntaxError";

        if (builtinBoolean) {
            declarations.append("pred true {}\npred false { not true }\n\n");
        }
        return declarations.toString();
    }

    private String predDec(int n) {
        StringBuilder sb = new StringBuilder("set _UNIV");
        for (int i = 0; i < n - 2; i++)
            sb.append(" -> set _UNIV");
        return sb.toString();
    }

    private String funDec(int n) {
        if (n == 1)
            return "one _UNIV";
        StringBuilder sb = new StringBuilder("set _UNIV");
        for (int i = 0; i < n - 2; i++)
            sb.append(" -> set _UNIV");
        sb.append(" -> one _UNIV");
        return sb.toString();
    }

    @Override
    public String visitSpec(FOFTPTPParser.SpecContext ctx) {
        StringBuilder includes = new StringBuilder("");
        StringBuilder facts = new StringBuilder("fact{\n");
        for (FOFTPTPParser.LineContext n : ctx.line())
            if (n instanceof FOFTPTPParser.Fof_annotatedContext)
                facts.append("    " + visit(n) + "\n\n");
            else if (n instanceof FOFTPTPParser.IncludeContext)
                includes.append(visit(n) + "\n");
        facts.append("}\n");
        return includes.toString() + facts.toString();
    }

    @Override
    public String visitFof_annotated(FOFTPTPParser.Fof_annotatedContext ctx) {
        vars.clear();
        String f = visit(ctx.fof_formula());
        if (ctx.ID().getText().equals("conjecture"))
            return "(not " + f + ")";
        return f;
    }

    @Override
    public String visitInclude(FOFTPTPParser.IncludeContext ctx) {
        String inputFilePath = ctx.SINGLE_QUOTED().getText();
        // remove the surrounding single quotes
        inputFilePath = inputFilePath.substring(1, inputFilePath.length() - 1);
        // there is a danger here with infinite includes
        // but let's assume that won't happen
        String thy2;
        try {
            File f = new File(filePath);
            String root_directory = f.getParentFile().getParentFile().getParent();
            File f_include = new File(root_directory + "/" + inputFilePath);

            InputStream inputStream = new FileInputStream(f_include);
            CharStream stream = CharStreams.fromStream(inputStream);
            FOFTPTPLexer lexer = new FOFTPTPLexer(stream);
            CommonTokenStream tokens = new CommonTokenStream(lexer);
            FOFTPTPParser parser = new FOFTPTPParser(tokens);
            ParseTree tree = parser.spec();
            if (parser.getNumberOfSyntaxErrors() >= 1) {
                errorDuringImport = true;
                return "SyntaxError";
            }
            return this.visit(tree);
        } catch (Exception e) {
            errorDuringImport = true;
            return "SyntaxError: Something bad happened when parsing the imported file: " + inputFilePath;
        }
    }


    @Override
    public String visitNot(FOFTPTPParser.NotContext ctx) {
        return "(not " + visit(ctx.fof_formula()) + ")";
    }

    @Override
    public String visitForall(FOFTPTPParser.ForallContext ctx) {
        StringBuilder sb = new StringBuilder("(all ");
        sb.append(ctx.ID(0).getText() + "_");
        vars.add(ctx.ID(0).getText() + "_");
        final int len = ctx.ID().size();
        for (int i = 1; i != len; i++) {
            String name = ctx.ID(i).getText() + "_";
            vars.add(name);
            sb.append(", " + name);
        }
        sb.append(": " + univ + " | " + visit(ctx.fof_formula()) + ")");
        return sb.toString();
    }

    @Override
    public String visitExists(FOFTPTPParser.ExistsContext ctx) {
        StringBuilder sb = new StringBuilder("(some ");
        sb.append(ctx.ID(0).getText() + "_");
        vars.add(ctx.ID(0).getText() + "_");
        final int len = ctx.ID().size();
        for (int i = 1; i != len; i++) {
            String name = ctx.ID(i).getText() + "_";
            vars.add(name);
            sb.append(", " + name);
        }
        sb.append(": " + univ + " | " + visit(ctx.fof_formula()) + ")");
        return sb.toString();
    }

    @Override
    public String visitAnd(FOFTPTPParser.AndContext ctx) {
        return "(" + visit(ctx.fof_formula(0)) + " and " + visit(ctx.fof_formula(1)) + ")";
    }

    @Override
    public String visitOr(FOFTPTPParser.OrContext ctx) {
        return "(" + visit(ctx.fof_formula(0)) + " or " + visit(ctx.fof_formula(1)) + ")";
    }

    @Override
    public String visitImp(FOFTPTPParser.ImpContext ctx) {
        return "(" + visit(ctx.fof_formula(0)) + " implies " + visit(ctx.fof_formula(1)) + ")";
    }

    @Override
    public String visitIff(FOFTPTPParser.IffContext ctx) {
        return "(" + visit(ctx.fof_formula(0)) + " iff " + visit(ctx.fof_formula(1)) + ")";
    }

    @Override
    public String visitEq(FOFTPTPParser.EqContext ctx) {
        return "(" + visit(ctx.term(0)) + " = " + visit(ctx.term(1)) + ")";
    }

    @Override
    public String visitNeq(FOFTPTPParser.NeqContext ctx) {
        return "(not (" + visit(ctx.term(0)) + " = " + visit(ctx.term(1)) + "))";
    }

    @Override
    public String visitProp(FOFTPTPParser.PropContext ctx) {
        String temp = ctx.ID().getText() + "_";
        props.add(temp);
        return "(some " + temp + ")";
    }

    @Override
    public String visitDefined_prop(FOFTPTPParser.Defined_propContext ctx) {
        String name = ctx.DEFINED_PROP().getText();
        builtinBoolean = true;
        if (name.equals("$true"))
            return "true";
        else if (name.equals("$false"))
            return "false";
        return "";
    }

    @Override
    public String visitPred(FOFTPTPParser.PredContext ctx) {
        String name = ctx.ID().getText() + "_";
        final int len = ctx.term().size();
        if (len == 1)
            sets.add(name);
        else
            relSym.put(name, len);
        StringBuilder sb = new StringBuilder("((");
        sb.append(visit(ctx.term(0)));
        for (int i = 1; i != len; i++) {
            sb.append(' ');
            sb.append('-');
            sb.append('>');
            sb.append(' ');
            sb.append(visit(ctx.term(i)));
        }
        sb.append(") in " + name + ")");
        return sb.toString();
    }

    @Override
    public String visitParen(FOFTPTPParser.ParenContext ctx) {
        return "(" + visit(ctx.fof_formula()) + ")";
    }

    @Override
    public String visitConVar(FOFTPTPParser.ConVarContext ctx) {
        String name = ctx.ID().getText() + "_";
        if (!vars.contains(name)) {
            constants.add(name);
            //System.out.println("Adding " + name);
        }
        return name;
    }

    @Override
    public String visitApply(FOFTPTPParser.ApplyContext ctx) {
        String name = ctx.ID().getText() + "_";
        final int len = ctx.term().size();
        funSym.put(name, len);
        StringBuilder sb = new StringBuilder(name);
        sb.append('[');
        sb.append(visit(ctx.term(0)));
        for (int i = 1; i != len; i++) {
            sb.append(' ');
            sb.append(',');
            sb.append(visit(ctx.term(i)));
        }
        sb.append(']');
        return sb.toString();
    }
}