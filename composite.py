from component import Component
from typing import List
import pymysql
import pandas as pd


connection = pymysql.connect(host="localhost", user="root", passwd="", database="database")
cursor = connection.cursor()

class Composite(Component):
    """
    The Composite class represents the complex components that may have
    children. Usually, the Composite objects delegate the actual work to their
    children and then "sum-up" the result.
    """
    "The Folder class can contain other folders and files"

    def __init__(self,name) -> None:
        self._children: List[Component] = []
        self.name = name 
    """
    A composite object can add or remove other components (both simple or
    complex) to or from its child list.
    """

    def add(self, component: Component) -> None:
        self._children.append(component)
        component.parent = self

    def remove(self, component: Component) -> None:
        self._children.remove(component)
        component.parent = None

    def is_composite(self) -> bool:
        return True

    def operation(self) -> str:
        """
        The Composite executes its primary logic in a particular way. It
        traverses recursively through all its children, collecting and summing
        their results. Since the composite's children pass these calls to their
        children and so forth, the whole object tree is traversed as a result.
        """

        results = []
        for child in self._children:
            results.append(child.operation())
        return f"Branch({'+'.join(results)})"

    def set_SensorID(self) -> None:
        #database connection
        TableSql = """CREATE TABLE {}(
        ID INT(20) PRIMARY KEY AUTO_INCREMENT,
        NAME  CHAR(20) NOT NULL,
        Sensor_ID INT(6) NOT NULL)""".format(self.name)

        cursor.execute(TableSql)
        
        print('set sensor id for {}'.format(self.name))
        
        CPD_S = input(f"CPD_S  : ")
        AFPCS_S = input(f"AFPCS_S  : ")
        Tcd_C = input(f"Tcd_C  : ")
        Tci_C = input(f"Tci_C  : ")
        AFQ_S = input(f"AFQ_S  : ")
        GQBH_S = input(f"GQBH_S  : ")
        FQG_S = input(f"FQG_S  : ")
        TTRF_C = input(f"TTRF_C  : ")
        SPGR = input(f"SPGR  : ")
        FHHV_B = input(f"FHHV_B  : ")
        PLPSTL = input(f"PLPSTL  : ")
        GLPS_1 = input(f"GLPS_1  : ")
        TTXM_C = input(f"TTXM_C  : ")
        AFPEP_S = input(f"AFPEP_S  : ")

        mySql_insert_query = """INSERT INTO {table}(NAME, Sensor_ID) 
                           VALUES (%s, %s) """.format(table=self.name)

        records_to_insert = [('CPD_S','{}'.format(CPD_S)),('AFPCS_S','{}'.format(AFPCS_S)),('Tcd_C','{}'.format(Tcd_C)),('Tci_C','{}'.format(Tci_C)),('AFQ_S','{}'.format(AFQ_S)),('GQBH_S','{}'.format(GQBH_S))
                            ,('FQG_S','{}'.format(FQG_S)),('TTRF_C','{}'.format(TTRF_C)),('SPGR','{}'.format(SPGR)),('FHHV_B','{}'.format(FHHV_B)),('PLPSTL','{}'.format(PLPSTL)),('GLPS_1','{}'.format(GLPS_1))
                            ,('TTXM_C','{}'.format(TTXM_C)),('AFPEP_S','{}'.format(AFPEP_S))]
    

        cursor.executemany(mySql_insert_query, records_to_insert)
        connection.commit()
        # connection.close()

    def get_data(self) -> pd.DataFrame:

        # queries for retrievint all rows
        retrive = '''Select * from {}'''.format(self.name)
        #executing the quires
        cursor.execute(retrive)
        rows = cursor.fetchall()
        sensor_id = []

        for row in rows:
            sensor_id.append(row[2])
        print(sensor_id)
         # TODO need to check null value
        query_from_where = '''SELECT app_taghistory_subparams.y,app_taghistory_subparams.m,app_taghistory_subparams.d, app_taghistory_subparams.h,
    MAX(CASE WHEN app_taghistory_subparams.variabletag_id = {} THEN app_taghistory_subparams.value ELSE null END) "CPD_S",
    MAX(CASE WHEN app_taghistory_subparams.variabletag_id = {} THEN app_taghistory_subparams.value ELSE null END) "AFPCS_S",
    MAX(CASE WHEN app_taghistory_subparams.variabletag_id = {} THEN app_taghistory_subparams.value ELSE null END) "Tcd_C",
    MAX(CASE WHEN app_taghistory_subparams.variabletag_id = {} THEN app_taghistory_subparams.value ELSE null END) "Tci_C",
    MAX(CASE WHEN app_taghistory_subparams.variabletag_id = {} THEN app_taghistory_subparams.value ELSE null END) "AFQ_S",
    MAX(CASE WHEN app_taghistory_subparams.variabletag_id = {} THEN app_taghistory_subparams.value ELSE null END) "GQBH_S",
    MAX(CASE WHEN app_taghistory_subparams.variabletag_id = {} THEN app_taghistory_subparams.value ELSE null END) "FQG_S",
    MAX(CASE WHEN app_taghistory_subparams.variabletag_id = {} THEN app_taghistory_subparams.value ELSE null END) "TTRF_C",
    MAX(CASE WHEN app_taghistory_subparams.variabletag_id = {} THEN app_taghistory_subparams.value ELSE null END) "SPGR",
    MAX(CASE WHEN app_taghistory_subparams.variabletag_id = {} THEN app_taghistory_subparams.value ELSE null END) "FHHV_B",
    MAX(CASE WHEN app_taghistory_subparams.variabletag_id = {} THEN app_taghistory_subparams.value ELSE null END) "PLPSTL",
    MAX(CASE WHEN app_taghistory_subparams.variabletag_id = {} THEN app_taghistory_subparams.value ELSE null END) "GLPS_1",
    MAX(CASE WHEN app_taghistory_subparams.variabletag_id = {} THEN app_taghistory_subparams.value ELSE null END) "TTXM_C",
    MAX(CASE WHEN app_taghistory_subparams.variabletag_id = {} THEN app_taghistory_subparams.value ELSE null END) "AFPEP_S"
    FROM app_taghistory_subparams
    GROUP BY year(app_taghistory_subparams.timestamp),month(app_taghistory_subparams.timestamp),day(app_taghistory_subparams.timestamp), hour(app_taghistory_subparams.timestamp)
    ORDER BY year(app_taghistory_subparams.timestamp),month(app_taghistory_subparams.timestamp),day(app_taghistory_subparams.timestamp), hour(app_taghistory_subparams.timestamp)
    '''.format(sensor_id[0],sensor_id[1],sensor_id[2],sensor_id[3],sensor_id[4],sensor_id[5],sensor_id[6],sensor_id[7],sensor_id[8],sensor_id[9],sensor_id[10],sensor_id[11],sensor_id[12],sensor_id[13])

        cursor.execute(query_from_where)
        tags_data = cursor.fetchall()

    def set_supparam(self) -> None:
        #database connection
        TableSql = """CREATE TABLE input(
        ID INT(20) PRIMARY KEY AUTO_INCREMENT,
        NAME  CHAR(20) NOT NULL,
        Sensor_ID INT(6) NOT NULL,
        supparam INT(50))"""

        cursor.execute(TableSql)
        
    

        mySql_insert_query = """INSERT INTO input(NAME, supparam) 
                           VALUES (%s, %s) """

        records_to_insert = [('CPD_S',253),('AFPCS_S',434),('Tcd_C',848),('Tci_C',754),('AFQ_S',34),('GQBH_S',252)
                            ,('FQG_S',724),('TTRF_C',471),('SPGR',774),('FHHV_B',775),('PLPSTL',1411),('GLPS_1',245)
                            ,('TTXM_C',123),('AFPEP_S',754)]
    

        cursor.executemany(mySql_insert_query, records_to_insert)
        connection.commit()