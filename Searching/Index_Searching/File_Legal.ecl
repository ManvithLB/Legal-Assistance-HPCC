EXPORT File_Legal := MODULE
 
 EXPORT Layout1 := RECORD
  STRING10 field;
  UNSIGNED8 text_id;
  STRING32700 text;
 END;
 
 EXPORT File1 := DATASET('~legal::ildc_multi_text_id',Layout1,CSV);
 
 EXPORT Layout2 := RECORD
  STRING field;
  UNSIGNED8 text_id;
  STRING100 words;
 END;
 
 EXPORT File2 := DATASET('~legal::ildc_multi_words',Layout2,CSV);
 
 EXPORT Layout3 := RECORD
  STRING100 words;
 END;
 
 EXPORT File3 := DATASET('~legal::test_words',Layout3,CSV);
 
END;