*&---------------------------------------------------------------------*
*& Data Declaration
*&---------------------------------------------------------------------*
DATA: gv_formname   TYPE tdsfname VALUE 'ZZDEMO', "Give the name of the smartform
      gv_fm_name    TYPE rs38l_fnam.
DATA: gwa_ssfcompop TYPE ssfcompop,
      gv_control_parameters    TYPE ssfctrlop.
DATA: gv_output_options    TYPE rspoptype.


*&---------------------------------------------------------------------*
*& START-OF-SELECTION
*&---------------------------------------------------------------------*
START-OF-SELECTION.
*Get the function module name using form name
  CALL FUNCTION 'SSF_FUNCTION_MODULE_NAME'
    EXPORTING
      formname           = gv_formname
    IMPORTING
      fm_name            = gv_fm_name
    EXCEPTIONS
      no_form            = 1
      no_function_module = 2
      OTHERS             = 3.
  IF sy-subrc <> 0.
    MESSAGE ID sy-msgid TYPE sy-msgty NUMBER sy-msgno
            WITH sy-msgv1 sy-msgv2 sy-msgv3 sy-msgv4.
  ENDIF.

*Get Device Type
  CALL FUNCTION 'SSF_GET_DEVICE_TYPE'
    EXPORTING
      i_language             = sy-langu
    IMPORTING
      e_devtype              = gv_output_options
    EXCEPTIONS
      no_language            = 1
      language_not_installed = 2
      no_devtype_found       = 3
      system_error           = 4
      OTHERS                 = 5.

  gwa_ssfcompop-tdprinter = gv_output_options.
*Suppress print dialog
* gv_control_parameters -no_dialog = 'X'.
* Enable print preview
* gv_control_parameters -preview = 'X'.

*Trigger the smartform
  CALL FUNCTION gv_fm_name
    EXPORTING
      control_parameters = gv_control_parameters 
      output_options     = gwa_ssfcompop
    EXCEPTIONS
      formatting_error   = 1
      internal_error     = 2
      send_error         = 3
      user_canceled      = 4
      OTHERS             = 5.
  IF sy-subrc <> 0.
    MESSAGE ID sy-msgid TYPE sy-msgty NUMBER sy-msgno
            WITH sy-msgv1 sy-msgv2 sy-msgv3 sy-msgv4.
  ENDIF.
