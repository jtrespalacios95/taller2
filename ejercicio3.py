import pandas as pd

def calculate_elapsed_time(time):
    if ":" in time:
        minutes , seconds = str(time).split(":",1)
        return (float(minutes) * 60 * 1000) + float(seconds) * 1000
    return time

def assing_trunk(field):
    return df[df[field].isna() != True][
        field].str.strip().str.split(
        ",").str

df = pd.read_csv("entrrada.csv",sep="|")

llaves_iguales = ['Call type','Date','Time','Carrier connect date','Carrier connect time','Carrier elapsed time','Sensor_Type',
                 'Sensor_ID','Recording Office_Type','Recording Office_ID','Timing indicator','Study indicator','Service observed / Traffic sampled','Operator action',
                 'Service feature code','Overseas indicator','IC / INC indicator','IC/INC call event status','IC / INC Routing Indicator','Dialing and presubscription indicator',
                 'ANI / CPN indicator']

df_exportar = df[llaves_iguales].copy()

diccionario_tipo = {5:"Local message rate call",110:"Interlata call",119:"Incoming CDR",90:None}

df_exportar["Type"] = df["Call type"].apply(lambda x: diccionario_tipo[x])

df["Trunk_Id_R0"], df["Trunk_Id_R1"] =   assing_trunk("Trunk Identification_Routing Indicator")
df["Trunk_Id_Group_N0"], df["Trunk_Id_Group_N1"] = assing_trunk("Trunk Identification_Trunk Group Number")

df["Trunk_Id_Member_N0"], df["Trunk_Id_Member_N1"] = assing_trunk("Trunk Identification_Trunk Member Number")

df_exportar["m104.trunkid"] = df["Trunk_Id_R0"].astype(str) + ":" + df["Trunk_Id_Group_N0"].astype(str) + ":" + df["Trunk_Id_Member_N0"].astype(str)
df_exportar["m104.trunkid1"] = df["Trunk_Id_R1"].astype(str) + ":" + df["Trunk_Id_Group_N1"].astype(str) + ":" + df["Trunk_Id_Member_N1"].astype(str)

df_exportar["m104.trunkid"] = df_exportar["m104.trunkid"].str.replace("nan:nan:nan", "")
df_exportar["m104.trunkid1"] = df_exportar["m104.trunkid1"].str.replace("nan:nan:nan", "")

df_exportar["m119.trunkgroupinfo"] = df["Trunk Group_Trunk Group Number - Interoffice"]

df_exportar["originatingnpa"] = df["Calling number"].str[:3]
df_exportar["originatingnumber"] = df["Calling number"].str[4:12]
df_exportar["terminatingnpa"] = df["Called number"].str[:3]
df_exportar["terminatingnumber "] = df["Called number"].str[4:12]

df_exportar["elapsedtime"] = df["Length of call"].apply(lambda x: calculate_elapsed_time(str(x)))

df_exportar.to_csv('output_exercise.csv', index=False, sep='|')

