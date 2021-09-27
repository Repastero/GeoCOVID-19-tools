# -*- coding: utf-8 -*-

# Cantidad grupos etarios en modelo
AGE_GROUP_REPAST_COUNT = 5

# Equivalencia entre grupos etarios nomivac -> modelo
AGE_GROUP_EQUIV = {
    '<18'   : [1,  0,  0,   0,   0],
    '18-29' : [0,.58,.42,   0,   0],
    '30-39' : [0,  0,  1,   0,   0],
    '40-49' : [0,  0,  0,   1,   0],
    '50-59' : [0,  0,  0,   1,   0],
    '60-69' : [0,  0,  0,.534,.466],
    '70-79' : [0,  0,  0,   0,   1],
    '80-89' : [0,  0,  0,   0,   1],
    '90-99' : [0,  0,  0,   0,   1],
    '>=100' : [0,  0,  0,   0,   1],
    'S.I.'  : [0,  0,  0,   0,   0], # estos los ignoro
}

# Contador dosis por grupos etarios nomivac
VACCINE_AG_COUNTER = {
    '<18'   : 0,
    '18-29' : 0,
    '30-39' : 0,
    '40-49' : 0,
    '50-59' : 0,
    '60-69' : 0,
    '70-79' : 0,
    '80-89' : 0,
    '90-99' : 0,
    '>=100' : 0,
    'S.I.'  : 0, # estos los ignoro
}

# jurisdiccion_residencia_id : jurisdiccion_residencia
JURISDICCION_NOMI = {
    '30' : 'Entre Ríos',
    '82' : 'Santa Fe',
    '46' : 'La Rioja',
}

# jurisdiccion_residencia_id : depto_residencia_id : depto_residencia
DEPTO_NOMI = {
    '30' : {
        '049' : 'Gualeguay',
        '070' : 'La Paz',
        '035' : 'Federal',
        '008' : 'Colón',
        '084' : 'Paraná',
        '021' : 'Diamante',
        '098' : 'Uruguay',
        '077' : 'Nogoyá',
        '113' : 'Villaguay',
        '015' : 'Concordia',
        '028' : 'Federación',
        '091' : 'Tala',
        '042' : 'Feliciano',
        '056' : 'Gualeguaychú',
        '063' : 'Islas del Ibicuy',
        '105' : 'Victoria',
        '088' : 'San Salvador',
    },
    '82' : {
        '084' : 'Rosario',
        '091' : 'San Cristóbal',
        '063' : 'La Capital',
        '028' : 'Constitución',
        '049' : 'General Obligado',
        '105' : 'San Jerónimo',
        '056' : 'Iriondo',
        '077' : '9 de Julio',
        '014' : 'Caseros',
        '126' : 'San Martín',
        '070' : 'Las Colonias',
        '042' : 'General López',
        '133' : 'Vera',
        '119' : 'San Lorenzo',
        '021' : 'Castellanos',
        '112' : 'San Justo',
        '035' : 'Garay',
        '098' : 'San Javier',
        '007' : 'Belgrano',
    },
    '46' : {
        '014' : 'Capital',
        '042' : 'Chilecito',
        '119' : 'San Blas de los Sauces',
        '035' : 'Chamical',
        '084' : 'General Ocampo',
        '056' : 'General Angel V. Peñaloza',
        '063' : 'General Belgrano',
        '077' : 'General Lamadrid',
        '007' : 'Arauco',
        '112' : 'Rosario Vera Peñaloza',
        '028' : 'Coronel Felipe Varela',
        '070' : 'General Juan F. Quiroga',
        '091' : 'General San Martín',
        '021' : 'Castro Barros',
        '126' : 'Sanagasta',
        '105' : 'Independencia',
        '098' : 'Vinchina',
        '049' : 'Famatina',
    }
}

# jurisdiccion_residencia_id : depto_residencia : depto repast
DEPTO_REPAST = {
    '30' : {
        'Gualeguay'       : 'gualeguay',
        'La Paz'          : 'lapaz',
        'Federal'         : 'federal',
        'Colón'           : 'colon',
        'Paraná'          : 'parana',
        'Diamante'        : 'diamante',
        'Uruguay'         : 'uruguay',
        'Nogoyá'          : 'nogoya',
        'Villaguay'       : 'villaguay',
        'Concordia'       : 'concordia',
        'Federación'      : 'federacion',
        'Tala'            : 'tala',
        'Feliciano'       : 'feliciano',
        'Gualeguaychú'    : 'gualeguaychu',
        'Islas del Ibicuy': 'islasdelibicuy',
        'Victoria'        : 'victoria',
        'San Salvador'    : 'sansalvador',
    },
    '82' : {
        'Rosario'           : 'rosario',
        'San Cristóbal'     : 'sancristobal',
        'La Capital'        : 'lacapital',
        'Constitución'      : 'constitucion',
        'General Obligado'  : 'generalobligado',
        'San Jerónimo'      : 'sanjeronimo',
        'Iriondo'           : 'iriondo',
        '9 de Julio'        : '9dejulio',
        'Caseros'           : 'caseros',
        'San Martín'        : 'sanmartin',
        'Las Colonias'      : 'lascolonias',
        'General López'     : 'generallopez',
        'Vera'              : 'vera',
        'San Lorenzo'       : 'sanlorenzo',
        'Castellanos'       : 'castellanos',
        'San Justo'         : 'sanjusto',
        'Garay'             : 'garay',
        'San Javier'        : 'sanjavier',
        'Belgrano'          : 'belgrano',
    },
    '46' : { # inventado - desconocido
        'Capital'                   : 'capital',
        'Chilecito'                 : 'chilecito',
        'San Blas de los Sauces'    : 'sanblas',
        'Chamical'                  : 'chamical',
        'General Ocampo'            : 'generalocampo',
        'General Angel V. Peñaloza' : 'generalangel',
        'General Belgrano'          : 'generalbelgrano',
        'General Lamadrid'          : 'generallamadrid',
        'Arauco'                    : 'arauco',
        'Rosario Vera Peñaloza'     : 'rosariovera',
        'Coronel Felipe Varela'     : 'coronelfelipe',
        'General Juan F. Quiroga'   : 'quiroga',
        'General San Martín'        : 'sanmartin',
        'Castro Barros'             : 'castrobarros',
        'Sanagasta'                 : 'sanagasta',
        'Independencia'             : 'independencia',
        'Vinchina'                  : 'vinchina',
        'Famatina'                  : 'famatina',
    }
}

# jurisdiccion_residencia_id : depto repast
DEPTO_REPAST_POP = {
    '30' : {
        'gualeguay'     : 0.8290,
        'lapaz'         : 0.3858,
        'federal'       : 0.6966,
        'colon'         : 0.3995,
        'parana'        : 0.7292,
        'diamante'      : 0.4299,
        'uruguay'       : 0.7320,
        'nogoya'        : 0.6073,
        'villaguay'     : 0.7074,
        'concordia'     : 0.8956,
        'federacion'    : 0.5070,
        'tala'          : 0.5347,
        'feliciano'     : 0.8014,
        'gualeguaychu'  : 0.7593,
        'islasdelibicuy': 0.4057,
        'victoria'      : 0.8903,
        'sansalvador'   : 0.7621,
    },
    '82' : {
        '9dejulio'          : {'tostado' : 0.5338},
        'belgrano'          : {'lasparejas+lasrosas+armstrong' : 0.8569},
        'caseros'           : {'casilda' : 0.4492, 'sanjosedelaesquina+arequito+chabas' : 0.2471},
        'castellanos'       : {'rafaela' : 0.5265, 'sunchales' : 0.1232},
        'constitucion'      : {'villaconstitucion' : 0.5649},
        'garay'             : {'helvecia+santarosadecalchines+cayasta' : 0.8920},
        'generallopez'      : {'venadotuerto' : 0.4176, 'firmat' : 0.1078, 'rufino' : 0.0976, 'villacanas' : 0.0475},
        'generalobligado'   : {'reconquista' : 0.4317, 'villaocampo+lastoscas' : 0.1666, 'avellaneda' : 0.1556},
        'iriondo'           : {'canadadegomez' : 0.4380, 'totoras' : 0.1622},
        'lacapital'         : {'santafe' : 0.7344},
        'lascolonias'       : {'pilar+humboldt+esperanza' : 0.5150, 'sanjeronimonorte+franck+sancarloscentro' : 0.2178},
        'rosario'           : {'rosario' : 0.7742},
        'sancristobal'      : {'sanguillermo+suardi' : 0.2319, 'ceres' : 0.2305, 'sancristobal' : 0.2119},
        'sanjavier'         : {'sanjavier' : 0.5394, 'romang' : 0.2834},
        'sanjeronimo'       : {'desvioarijon+arocena+coronda' : 0.2965, 'galvez' : 0.2369, 'maciel+gaboto+monje+barrancas' : 0.2071, 'sangenaro+centeno' : 0.1445},
        'sanjusto'          : {'sanjusto' : 0.5577},
        'sanlorenzo'        : {'sanlorenzo+puertogeneralsanmartin' : 0.3744, 'capitanbermudez+frayluisbeltran' : 0.2763, 'carcarana+sanjeronimosud+roldan' : 0.2161},
        'sanmartin'         : {'eltrebol+carlospellegrini+canadarosquin+piamonte' : 0.4059, 'sanjorge+sastre' : 0.3753},
        'vera'              : {'vera+margarita+calchaqui' : 0.7232},
    },
    '46' : { # inventado - desconocido
        'capital'           : 0.75,
        'chilecito'         : 0.75,
        'sanblas'           : 0.75,
        'chamical'          : 0.75,
        'generalocampo'     : 0.75,
        'generalangel'      : 0.75,
        'generalbelgrano'   : 0.75,
        'generallamadrid'   : 0.75,
        'arauco'            : 0.75,
        'rosariovera'       : 0.75,
        'coronelfelipe'     : 0.75,
        'quiroga'           : 0.75,
        'sanmartin'         : 0.75,
        'castrobarros'      : 0.75,
        'sanagasta'         : 0.75,
        'independencia'     : 0.75,
        'vinchina'          : 0.75,
        'famatina'          : 0.75,
    }
}
