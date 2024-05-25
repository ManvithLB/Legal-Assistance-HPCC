#OPTION('outputLimit',650);
IMPORT $,STD;

rec1 := RECORD
STRING text_id;
STRING words;
END;

df1 := DATASET('~legal::words_with_id',rec1,THOR);

rec := RECORD
df1.text_id;
df1.words;
STRING100 words_lower := '';
END;

tb1 := TABLE(df1,rec);

tb1 doUpdate(tb1 le) := TRANSFORM
SELF.words_lower := STD.Str.ToLowerCase(le.words);
SELF := le;
END;

df2 := PROJECT(tb1,doUpdate(LEFT));

OUTPUT(df2,,'~legal::words_lower',OVERWRITE);
