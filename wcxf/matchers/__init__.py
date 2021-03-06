import wcxf
from . import smeft


@wcxf.matcher('SMEFT', 'Warsaw up', 'WET', 'JMS')
def warsaw_up_to_jms(C, scale, parameters):
    return smeft.match_all(C, parameters)


@wcxf.matcher('SMEFT', 'Warsaw', 'WET', 'JMS')
def warsaw_to_jms(C, scale, parameters):
    C_warsawup = wcxf.translators.smeft.warsaw_to_warsaw_up(C, parameters)
    return smeft.match_all(C_warsawup, parameters)


@wcxf.matcher('SMEFT', 'Warsaw', 'WET', 'flavio')
def warsaw_to_flavio(C, scale, parameters):
    C_warsawup = wcxf.translators.smeft.warsaw_to_warsaw_up(C, parameters)
    C_JMS = smeft.match_all(C_warsawup, parameters)
    return wcxf.translators.JMS_to_flavio(C_JMS, scale, parameters)


@wcxf.matcher('SMEFT', 'Warsaw', 'WET', 'EOS')
def warsaw_to_eos(C, scale, parameters):
    C_warsawup = wcxf.translators.smeft.warsaw_to_warsaw_up(C, parameters)
    C_JMS = smeft.match_all(C_warsawup, parameters)
    return wcxf.translators.JMS_to_EOS(C_JMS, scale, parameters)


@wcxf.matcher('SMEFT', 'Warsaw', 'WET', 'Bern')
def warsaw_to_bern(C, scale, parameters):
    C_warsawup = wcxf.translators.smeft.warsaw_to_warsaw_up(C, parameters)
    C_JMS = smeft.match_all(C_warsawup, parameters)
    return wcxf.translators.JMS_to_Bern(C_JMS, scale, parameters)


@wcxf.matcher('WET', 'flavio', 'WET-4', 'flavio')
def wet_wet4_flavio(C, scale, parameters):
    keys = wcxf.Basis['WET-4', 'flavio'].all_wcs
    return {k: v for k, v in C.items() if k in keys}


@wcxf.matcher('WET-4', 'flavio', 'WET-3', 'flavio')
def wet4_wet3_flavio(C, scale, parameters):
    keys = wcxf.Basis['WET-3', 'flavio'].all_wcs
    return {k: v for k, v in C.items() if k in keys}


@wcxf.matcher('WET', 'Bern', 'WET-4', 'Bern')
def wet_wet4_bern(C, scale, parameters):
    keys = wcxf.Basis['WET-4', 'Bern'].all_wcs
    return {k: v for k, v in C.items() if k in keys}


@wcxf.matcher('WET-4', 'Bern', 'WET-3', 'Bern')
def wet4_wet3_bern(C, scale, parameters):
    keys = wcxf.Basis['WET-3', 'Bern'].all_wcs
    return {k: v for k, v in C.items() if k in keys}


@wcxf.matcher('WET', 'JMS', 'WET-4', 'JMS')
def wet_wet4_jms(C, scale, parameters):
    keys = wcxf.Basis['WET-4', 'JMS'].all_wcs
    return {k: v for k, v in C.items() if k in keys}


@wcxf.matcher('WET-4', 'JMS', 'WET-3', 'JMS')
def wet4_wet3_jms(C, scale, parameters):
    keys = wcxf.Basis['WET-3', 'JMS'].all_wcs
    return {k: v for k, v in C.items() if k in keys}


@wcxf.matcher('WET-3', 'JMS', 'WET-2', 'JMS')
def wet3_wet2_jms(C, scale, parameters):
    keys = wcxf.Basis['WET-2', 'JMS'].all_wcs
    return {k: v for k, v in C.items() if k in keys}
