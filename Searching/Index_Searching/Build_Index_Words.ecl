EXPORT Build_Index_Words := MODULE

df := $.File_Legal.File2;

rec := RECORD
df.text_id;
df.words;
END;

EXPORT df1 := DATASET('~legal::words_with_id',{rec,UNSIGNED8 recpos {VIRTUAL(fileposition)}},THOR);

EXPORT idx := INDEX(df1,{text_id,words,recpos},'~legal::words_with_key');

EXPORT build_idx := BUILDINDEX(idx);

END;