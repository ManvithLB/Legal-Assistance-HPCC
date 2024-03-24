IMPORT $;

df1 := $.Build_Index_Words.df1;

idx1 := $.Build_Index_Words.idx;

df2 := $.File_Legal.File3;

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

OUTPUT(final_tb);

// base_df := $.Build_Index_Text.df1;

// idx2 := $.Build_Index_Text.idx;

// out_rec := RECORD
// UNSIGNED8 text_id;
// UNSIGNED2 count_id;
// STRING10000 text;
// END;

// out_rec doJoin2(final_tb le, base_df ri) := TRANSFORM
 // SELF := le;
 // SELF := ri;
// END;

// out := JOIN(final_tb,base_df,LEFT.text_id=RIGHT.text_id,doJoin2(LEFT,RIGHT),KEYED(idx2));

// out;