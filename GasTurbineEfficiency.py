##################################################
# Gas Turbine Efficiency
# A calculation module which consist of the following function:
#   1. Compressor Efficiency Calculate Function
#   2. Combustor Efficiency Calculate Function
#   3. Turbine Efficiency Calculate Function
#
# Revision Hisory (DD/MM/YYYY)
# 07/12/2020 - First init.
# 18/01/2021 - Implemented Combustor Efficiency Formula in combustor_efficiency function.
#
# TODO: [Important] Update tag parameter index.
# TODO: [Optional] Optimize tag parameter indexing and add error handling if neccessary
##################################################

#################### CONSTANTS ####################
# Compressor Efficiency Function Parameter Index
COMPRESSOR_CPD_S_INDEX = 4    #compressor discharge pressure (barg)
COMPRESSOR_AFPCS_S_INDEX = 5  #compressor inlet pressure (mbarg)
COMPRESSOR_Tcd_C_INDEX = 6    #compressor discharge temperature (median) (deg C)
COMPRESSOR_Tci_C_INDEX = 7    #compressor inlet temperature (median) (deg C)

# Combustor Efficiency Function Parameter Index
COMBUSTOR_CPD_S_INDEX = 4     #compressor discharge pressure (barg)
COMBUSTOR_Tcd_C_INDEX = 6     #compressor discharge temperature (deg C)
COMBUSTOR_AFQ_S_INDEX = 8     #Compressor inlet flow rate  (KG/s)
COMBUSTOR_GQBH_S_INDEX = 9    #IBH flow rate (KG/s)
COMBUSTOR_FQG_S_INDEX = 10    #Fuel consumption (KG/s)
COMBUSTOR_TTRF_C_INDEX = 11   #Turbine inlet air flow (deg C)
COMBUSTOR_SPGR_INDEX = 12     #Specific gravity (air = 1)
COMBUSTOR_FHHV_B_INDEX = 13   #Fuel gas HHV (BTU/SF3)

# Turbine Efficiency Function Parameter Index
TURBINE_TTXM_C_INDEX = 14     #gas turbine exhaust temperature (deg C)
TURBINE_TTRF1_C_INDEX = 11    #turbine inlet temperature (deg C)
TURBINE_AFPEP_S_INDEX = 15    #gas turbine exhaust pressure (mbarg)
TURBINE_CPD_S_INDEX = 4       #compressor discharge pressure (barg)

###################################################
import numpy as np
Pa = np.array([ 10000, 50000, 100000, 500000, 1000000, 1500000, 2000000, 2500000, 3000000  ])

K = np.array([ 260, 273.15, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 550, 560, 580, 600, 620, 640, 650, 660, 680, 700, 750, 800, 850, 900, 950, 1000, 1100, 1200, 1300, 1400, 1500 ])

z = np.array( [
    [1.401, 1.401, 1.401, 1.400, 1.400, 1.399, 1.398, 1.397, 1.395, 1.394, 1.392, 1.391, 1.389, 1.387, 1.385, 1.383, 1.381, 1.380, 1.378, 1.376, 1.374, 1.371, 1.370, 1.369, 1.367, 1.365, 1.359, 1.354, 1.349, 1.344, 1.340, 1.336, 1.329, 1.324, 1.319, 1.314, 1.311],
    [1.402, 1.402, 1.401, 1.401, 1.400, 1.399, 1.398, 1.397, 1.396, 1.394, 1.393, 1.391, 1.389, 1.387, 1.385, 1.383, 1.382, 1.381, 1.378, 1.376, 1.374, 1.371, 1.370, 1.369, 1.367, 1.365, 1.359, 1.354, 1.349, 1.344, 1.340, 1.336, 1.329, 1.324, 1.319, 1.314, 1.311],
    [1.403, 1.403, 1.402, 1.402, 1.401, 1.400, 1.399, 1.398, 1.396, 1.395, 1.393, 1.391, 1.389, 1.387, 1.385, 1.383, 1.382, 1.381, 1.378, 1.376, 1.374, 1.372, 1.370, 1.369, 1.367, 1.365, 1.359, 1.354, 1.349, 1.344, 1.340, 1.336, 1.329, 1.324, 1.319, 1.314, 1.311],
    [1.412, 1.411, 1.410, 1.408, 1.406, 1.405, 1.403, 1.401, 1.400, 1.398, 1.396, 1.394, 1.392, 1.389, 1.387, 1.385, 1.384, 1.382, 1.380, 1.378, 1.375, 1.373, 1.372, 1.370, 1.368, 1.366, 1.360, 1.355, 1.350, 1.345, 1.341, 1.337, 1.330, 1.324, 1.319, 1.315, 1.311],
    [1.424, 1.421, 1.420, 1.416, 1.414, 1.411, 1.409, 1.406, 1.404, 1.402, 1.399, 1.397, 1.394, 1.392, 1.389, 1.387, 1.386, 1.384, 1.382, 1.379, 1.377, 1.374, 1.373, 1.372, 1.369, 1.367, 1.361, 1.356, 1.351, 1.346, 1.341, 1.337, 1.330, 1.324, 1.319, 1.315, 1.311],
    [1.436, 1.432, 1.430, 1.425, 1.421, 1.417, 1.414, 1.411, 1.408, 1.405, 1.403, 1.400, 1.397, 1.394, 1.392, 1.389, 1.388, 1.386, 1.384, 1.381, 1.378, 1.376, 1.374, 1.373, 1.371, 1.368, 1.362, 1.357, 1.351, 1.346, 1.342, 1.338, 1.331, 1.325, 1.320, 1.315, 1.311],
    [1.448, 1.443, 1.440, 1.433, 1.428, 1.424, 1.420, 1.416, 1.412, 1.409, 1.406, 1.403, 1.400, 1.397, 1.394, 1.391, 1.390, 1.388, 1.386, 1.383, 1.380, 1.377, 1.376, 1.375, 1.372, 1.369, 1.363, 1.357, 1.352, 1.347, 1.343, 1.338, 1.331, 1.325, 1.320, 1.315, 1.312],
    [1.461, 1.453, 1.450, 1.442, 1.435, 1.430, 1.425, 1.421, 1.417, 1.413, 1.410, 1.406, 1.403, 1.400, 1.397, 1.393, 1.392, 1.390, 1.387, 1.384, 1.382, 1.379, 1.377, 1.376, 1.373, 1.371, 1.364, 1.358, 1.353, 1.348, 1.343, 1.339, 1.332, 1.325, 1.320, 1.316, 1.312],
    [1.431, 1.465, 1.461, 1.451, 1.443, 1.436, 1.431, 1.426, 1.421, 1.417, 1.413, 1.409, 1.406, 1.042, 1.399, 1.396, 1.394, 1.392, 1.389, 1.386, 1.383, 1.380, 1.379, 1.377, 1.374, 1.372, 1.365, 1.359, 1.354, 1.348, 1.344, 1.339, 1.332, 1.325, 1.320, 1.316, 1.312]
    ] ).reshape( ( 9, 37 ) )

specific_heat = np.array([
    [1.004, 1.005, 1.005, 1.006, 1.007, 1.008, 1.010, 1.012, 1.014, 1.017, 1.020, 1.023, 1.026, 1.030, 1.034, 1.038, 1.040, 1.043, 1.047, 1.052, 1.056, 1.061, 1.063, 1.066, 1.071, 1.075, 1.087, 1.099, 1.111, 1.121, 1.132, 1.142, 1.160, 1.175, 1.189, 1.201, 1.212],
    [1.005, 1.005, 1.006, 1.006, 1.007, 1.008, 1.010, 1.012, 1.014, 1.017, 1.020, 1.023, 1.027, 1.030, 1.034, 1.038, 1.041, 1.043, 1.047, 1.052, 1.056, 1.061, 1.064, 1.066, 1.071, 1.076, 1.088, 1.099, 1.111, 1.122, 1.132, 1.142, 1.160, 1.175, 1.189, 1.201, 1.212],
    [1.007, 1.007, 1.007, 1.007, 1.008, 1.009, 1.011, 1.012, 1.015, 1.017, 1.020, 1.023, 1.027, 1.031, 1.034, 1.039, 1.041, 1.043, 1.047, 1.052, 1.057, 1.061, 1.064, 1.066, 1.071, 1.076, 1.088, 1.099, 1.111, 1.122, 1.132, 1.142, 1.160, 1.175, 1.189, 1.201, 2.212],
    [1.016, 1.015, 1.015, 1.014, 1.013, 1.014, 1.014, 1.016, 1.018, 1.020, 1.023, 1.025, 1.029, 1.032, 1.036, 1.040, 1.042, 1.044, 1.049, 1.053, 1.058, 1.062, 1.065, 1.067, 1.072, 1.076, 1.088, 1.100, 1.111, 1.122, 1.132, 1.142, 1.160, 1.176, 1.189, 1.201, 1.212],
    [1.029, 1.026, 1.024, 1.022, 1.020, 1.019, 1.019, 1.020, 1.021, 1.023, 1.025, 1.028, 1.031, 1.034, 1.038, 1.042, 1.044, 1.046, 1.050, 1.054, 1.059, 1.063, 1.066, 1.068, 1.073, 1.077, 1.089, 1.101, 1.112, 1.123, 1.133, 1.143, 1.160, 1.176, 1.190, 1.202, 1.212],
    [1.041, 1.036, 1.034, 1.030, 1.027, 1.025, 1.024, 1.024, 1.025, 1.026, 1.028, 1.031, 1.033, 1.037, 1.040, 1.044, 1.046, 1.047, 1.052, 1.056, 1.060, 1.065, 1.067, 1.069, 1.074, 1.078, 1.090, 1.101, 1.113, 1.123, 1.133, 1.143, 1.161, 1.176, 1.190, 1.202, 1.212],
    [1.054, 1.047, 1.044, 1.038, 1.034, 1.031, 1.029, 1.029, 1.029, 1.030, 1.031, 1.033, 1.036, 1.039, 1.042, 1.045, 1.047, 1.049, 1.052, 1.057, 1.061, 1.066, 1.068, 1.070, 1.075, 1.079, 1.091, 1.102, 1.113, 1.124, 1.134, 1.144, 1.161, 1.177, 1.190, 1.202, 1.213],
    [1.066, 1.058, 1.054, 1.046, 1.040, 1.036, 1.034, 1.033, 1.033, 1.033, 1.034, 1.036, 1.038, 1.041, 1.044, 1.047, 1.049, 1.051, 1.055, 1.059, 1.063, 1.067, 1.069, 1.071, 1.076, 1.080, 1.092, 1.103, 1.114, 1.124, 1.134, 1.144, 1.161, 1.177, 1.190, 1.202, 1.213],
    [1.079, 1.069, 1.064, 1.054, 1.047, 1.042, 1.039, 1.037, 1.036, 1.036, 1.037, 1.038, 1.040, 1.043, 1.046, 1.049, 1.051, 1.052, 1.056, 1.060, 1.064, 1.068, 1.070, 1.073, 1.077, 1.081, 1.093, 1.104, 1.115, 1.125, 1.135, 1.144, 1.162, 1.177, 1.191, 1.202, 1.213]
]).reshape((9,37))


def lookupTable(x0, y0):
    xi = np.abs(Pa-x0).argmin()
    yi = np.abs(K-y0).argmin()
    return xi,yi

def compressor_efficiency(compressor_tag_data, comp_no):
    """
    Compressor Efficiency Calculate Function
    :param: compressor_tag_data, k_air
    :param_type: list, float
    :return: eff_result
    :return_type: float
    """
    
    disable_cal = 0 
    for x in compressor_tag_data:  
        if x == None: 
            disable_cal = 1
            return None
            
    if disable_cal == 0: 
        if comp_no == 1:
            CPD_S = compressor_tag_data[COMPRESSOR_CPD_S_INDEX]
            AFPCS_S = compressor_tag_data[COMPRESSOR_AFPCS_S_INDEX]
            Tcd_C = compressor_tag_data[COMPRESSOR_Tcd_C_INDEX]
            Tci_C = compressor_tag_data[COMPRESSOR_Tci_C_INDEX]
            x1,y1 = lookupTable((CPD_S + AFPCS_S)/2, (Tcd_C + Tci_C)/2 + 273.15)
            k_air = z[x1,y1]
            k_air_power = (k_air - 1 ) / k_air
            if AFPCS_S == 0:
                return None
            numerator = ((CPD_S/AFPCS_S) ** (k_air_power)) - 1.00
            denominator = ((Tcd_C + 273.15) / (Tci_C + 273.15)) - 1.00            
            eff_result = (numerator / denominator ) * 100.00
        elif comp_no == 2:
            CPD_S = compressor_tag_data[COMPRESSOR_CPD_S_INDEX]
            AFPCS_S = compressor_tag_data[COMPRESSOR_AFPCS_S_INDEX]
            Tcd_C = compressor_tag_data[COMPRESSOR_Tcd_C_INDEX]
            Tci_C = compressor_tag_data[COMPRESSOR_Tci_C_INDEX]
            x1,y1 = lookupTable((CPD_S + AFPCS_S)/2, (Tcd_C + Tci_C)/2 + 273.15)
            k_air = z[x1,y1]
            k_air_power = (k_air - 1 ) / k_air
            if AFPCS_S == 0:
                return None            
            numerator = ((CPD_S/AFPCS_S) ** (k_air_power)) - 1.00
            if AFPCS_S == 0:
                return None
            denominator = ((Tcd_C + 273.15) / (Tci_C + 273.15)) - 1.00            
            eff_result = (numerator / denominator ) * 100.00           
        return k_air, k_air_power, numerator, denominator, eff_result

def combustor_efficiency(combustor_tag_data, comb_no):
    """
    Combuster Efficiency Calculate Function
    :param: combustor_tag_data
    :param_type: list
    :return: eff_result
    :return_type: float
    """
    
    disable_cal = 0 
    for x in combustor_tag_data:  
        if x == None: 
            disable_cal = 1
            return None
            
    if disable_cal == 0: 
        if comb_no == 1:
            CPD_S = combustor_tag_data[COMBUSTOR_CPD_S_INDEX]
            Tcd_C = combustor_tag_data[COMBUSTOR_Tcd_C_INDEX]
            AFQ_S = combustor_tag_data[COMBUSTOR_AFQ_S_INDEX]
            GQBH_S = combustor_tag_data[COMBUSTOR_GQBH_S_INDEX]
            FQG_S = combustor_tag_data[COMBUSTOR_FQG_S_INDEX]
            TTRF_C = combustor_tag_data[COMBUSTOR_TTRF_C_INDEX]
            SPGR = combustor_tag_data[COMBUSTOR_SPGR_INDEX]
            FHHV_B = combustor_tag_data[COMBUSTOR_FHHV_B_INDEX]

            # Formula
            # numerator = (CPAIR)((GCOMB + GFUEL_K)(TTRF1C + 273.15) - (GCOMB)(TdcC + 273.15))
            # denominator = GFULEK * FHHVJ
            # GFUELK = FQG_S * 3600
            # GCOMB == GIBH_K
            # GIBH_K = GQBH_S * 3600
            # CPAIR = CPAIRF(Pcd_PA, Tcd_C + 273.15)

            x1,y1 = lookupTable(CPD_S, Tcd_C + 273.15)
            CPAIR = specific_heat[x1,y1]
            numerator = CPAIR * ((((GQBH_S * 3600) + (FQG_S * 3600)) * (TTRF_C + 273.15)) - (GQBH_S * (Tcd_C + 273.15)))
            denominator = FQG_S * 3600 * FHHV_B
            if denominator ==0 :
                return None
            eff_result = (numerator / denominator ) * 100.00
        elif comb_no == 2:
            CPD_S = combustor_tag_data[COMBUSTOR_CPD_S_INDEX]
            Tcd_C = combustor_tag_data[COMBUSTOR_Tcd_C_INDEX]
            AFQ_S = combustor_tag_data[COMBUSTOR_AFQ_S_INDEX]
            GQBH_S = combustor_tag_data[COMBUSTOR_GQBH_S_INDEX]
            FQG_S = combustor_tag_data[COMBUSTOR_FQG_S_INDEX]
            TTRF_C = combustor_tag_data[COMBUSTOR_TTRF_C_INDEX]
            SPGR = combustor_tag_data[COMBUSTOR_SPGR_INDEX]
            FHHV_B = combustor_tag_data[COMBUSTOR_FHHV_B_INDEX]

            # Formula
            # numerator = (CPAIR)((GCOMB + GFUEL_K)(TTRF1C + 273.15) - (GCOMB)(TdcC + 273.15))
            # denominator = GFULEK * FHHVJ
            # GFUELK = FQG_S * 3600
            # GCOMB == GIBH_K
            # GIBH_K = GQBH_S * 3600
            # CPAIR = CPAIRF(Pcd_PA, Tcd_C + 273.15)

            x1,y1 = lookupTable(CPD_S, Tcd_C + 273.15)
            CPAIR = specific_heat[x1,y1]
            numerator = CPAIR * ((((GQBH_S * 3600) + (FQG_S * 3600)) * (TTRF_C + 273.15)) - (GQBH_S * (Tcd_C + 273.15)))
            denominator = FQG_S * 3600 * FHHV_B
            if denominator == 0:
                return None
            eff_result = (numerator / denominator ) * 100.00
       
        return CPAIR, numerator, denominator, eff_result

#def turbine_efficiency(turbine_tag_data, k_air):
def turbine_efficiency(turbine_tag_data, turb_no):
    """
    Turbine Efficiency Calculate Function
    :param: turbine_tag_data, k_air
    :param_type: list, float
    :return: eff_result
    :return_type: float
    """

    #disable_cal = 0 
    for x in turbine_tag_data:  
        if x == None: 
            #disable_cal = 1
            return None

    print(turbine_tag_data)  
    #if disable_cal == 0: 
    if turb_no == 1:
        TTXM_C = turbine_tag_data[TURBINE_TTXM_C_INDEX]
        TTRF1_C = turbine_tag_data[TURBINE_TTRF1_C_INDEX]
        AFPEP_S = turbine_tag_data[TURBINE_AFPEP_S_INDEX]
        CPD_S = turbine_tag_data[TURBINE_CPD_S_INDEX]
        print(TTXM_C,TTRF1_C,AFPEP_S,CPD_S)
        #Pcd_PA = x[0] * pow(10,5) + 101325
        # AFPEP_S = turbine_tag_data[COMPRESSOR_Tcd_C_INDEX] * pow(10,5) + 101325
        Pex_PA = turbine_tag_data[TURBINE_AFPEP_S_INDEX] * pow(10,5) + 101325
        #
        #Pci_PA = x[1] * pow(10,2) + 101325
        # CPD_S = turbine_tag_data[COMPRESSOR_Tci_C_INDEX] * pow(10,5) + 101325
        Pcd_PA = turbine_tag_data[TURBINE_CPD_S_INDEX] * pow(10,5) + 101325
        
        #Wrong value at lookup table
        # x1,y1 = lookupTable((AFPEP_S + CPD_S)/2, (turbine_tag_data[2] + turbine_tag_data[3])/2 + 273.15)
        x1,y1 = lookupTable((Pcd_PA + Pex_PA)/2, (turbine_tag_data[2] + turbine_tag_data[3])/2 + 273.15)
        k_air = z[x1,y1]
        
        k_air_power = (k_air - 1 ) / k_air
        numerator = (1 - (TTRF1_C + 273.15)) / (TTXM_C + 273.15)
        if CPD_S == 0:
            return None
        denominator = (1 - (AFPEP_S / (CPD_S * 0.95))) ** k_air_power
        if denominator == 0:
            return None
        eff_result = (numerator / denominator ) * 100.00
    elif turb_no == 2:
        TTXM_C = turbine_tag_data[TURBINE_TTXM_C_INDEX]
        TTRF1_C = turbine_tag_data[TURBINE_TTRF1_C_INDEX]
        AFPEP_S = turbine_tag_data[TURBINE_AFPEP_S_INDEX]
        CPD_S = turbine_tag_data[TURBINE_CPD_S_INDEX]

        #Pcd_PA = x[0] * pow(10,5) + 101325
        # AFPEP_S = turbine_tag_data[COMPRESSOR_Tcd_C_INDEX] * pow(10,5) + 101325
        Pex_PA = turbine_tag_data[TURBINE_AFPEP_S_INDEX] * pow(10,5) + 101325
        #
        #Pci_PA = x[1] * pow(10,2) + 101325
        # CPD_S = turbine_tag_data[COMPRESSOR_Tci_C_INDEX] * pow(10,5) + 101325
        Pcd_PA = turbine_tag_data[TURBINE_CPD_S_INDEX] * pow(10,5) + 101325
        
        #Wrong value at lookup table
        # x1,y1 = lookupTable((AFPEP_S + CPD_S)/2, (turbine_tag_data[2] + turbine_tag_data[3])/2 + 273.15)
        x1,y1 = lookupTable((Pcd_PA + Pex_PA)/2, (turbine_tag_data[2] + turbine_tag_data[3])/2 + 273.15)
        k_air = z[x1,y1]
        
        k_air_power = (k_air - 1 ) / k_air
        numerator = (1 - (TTRF1_C + 273.15)) / (TTXM_C + 273.15)
        if CPD_S == 0:
            return None
        denominator = (1 - (AFPEP_S / (CPD_S * 0.95))) ** k_air_power
        if (denominator ==0):
            return None
        eff_result = (numerator / denominator ) * 100.00       
    return k_air, k_air_power, denominator, eff_result
