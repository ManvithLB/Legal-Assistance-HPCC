IMPORT $;
IMPORT PYTHON3 as PY;

DATASET($.File_Legal.Layout3) test1(STRING T) := EMBED(PY)
  
words_list = T.split(',')

tuple_result = tuple(words_list) 
 
return tuple_result;
  
ENDEMBED;

EXPORT roxie_search() := FUNCTION

STRING Tex := '' : STORED('Enter_Words_with_comma');

base_df := $.File_Legal.File1;

df2 := test1(Tex);

df1 := $.Build_Index_Words.df1;

idx1 := $.Build_Index_Words.idx;

final_rec := RECORD
UNSIGNED8 text_id;
STRING100 words;
END;

final_rec doJoin(df2 le, df1 ri) := TRANSFORM
 SELF := le;
 SELF := ri;
END;

final := JOIN(df2,df1,LEFT.words=RIGHT.words,doJoin(LEFT,RIGHT),KEYED(idx1));

new_rec := RECORD
final.text_id;
UNSIGNED4 count_id := COUNT(GROUP);
END;

final_tb := SORT(TABLE(final,new_rec,text_id),-count_id)[1..10];

text_rec := RECORD
 UNSIGNED text_id;
 UNSIGNED count_id;
 STRING text;
END;

get_text := JOIN(final_tb,base_df,LEFT.text_id=RIGHT.text_id,
                  TRANSFORM(text_rec,
                  SELF := RIGHT,
                  SELF := LEFT),
                  INNER);

RETURN OUTPUT(get_text);

END;