
*******************************************************
** Round down when <= 5
*******************************************************



****************** Test
DATA: LS_VALS TYPE P DECIMALS 6 VALUE '594.86595'.
PERFORM format_round CHANGING LS_VALS.




*******************************************************
** Round function
*******************************************************
FORM format_round CHANGING dec_value TYPE P.
  DATA : num1         TYPE p DECIMALS 8,
         count_dec    TYPE i VALUE 6,
         bf_count_dec TYPE i VALUE 6,
         int_dec      TYPE i,
         i_frac       TYPE string,
         i_trunc      TYPE string,
         tm_char      TYPE c.

  num1 = dec_value.
  i_frac = frac( num1 ).

  DO 5 TIMES.

    IF count_dec > 3.

      int_dec = substring( val = i_frac off = count_dec len = 1 ).

      IF int_dec > 5.
        bf_count_dec = count_dec - 1.
        int_dec = substring( val = i_frac off = bf_count_dec len = 1 ).
        int_dec = int_dec + 1.
        tm_char = int_dec.
        REPLACE SECTION OFFSET count_dec LENGTH 1 OF: i_frac WITH '0'.
        REPLACE SECTION OFFSET bf_count_dec LENGTH 1 OF: i_frac WITH tm_char.
      ELSE.
        REPLACE SECTION OFFSET count_dec LENGTH 1 OF: i_frac WITH '0'.
      ENDIF.

      count_dec = count_dec - 1.
    ENDIF.
  ENDDO.
  i_trunc = trunc( num1 ).

  CONCATENATE i_trunc i_frac+1(03) INTO i_frac.
  CONDENSE i_frac NO-GAPS.
  dec_value = i_frac.
ENDFORM.
