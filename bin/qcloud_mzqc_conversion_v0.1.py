import os
import json
import pronto
import datetime
from typing import List, Dict, Set, Any, Optional, Callable 
from collections import defaultdict
from MZQC import MZQCFile as mzqc
import click

@click.command()
@click.option('-input', help='<path to the json>', required=True)
@click.option('-output', help='<path fot the resulting mzqc>', required=True)
def convert_to_mzqc(input, output):
    qccv = pronto.Ontology('https://raw.githubusercontent.com/HUPO-PSI/mzQC/master/cv/qc-cv.obo')
    psims = pronto.Ontology('https://raw.githubusercontent.com/HUPO-PSI/psi-ms-CV/master/psi-ms.obo')
    name_indexed = {qccv[x].name: qccv[x] for x in qccv}

    with open(input, "r") as f:
        qcloud = json.load(f)
        qcn = os.path.basename(f.name)

    base_name: str = qcn
    cmpltn: str = str(datetime.datetime.now())  # dummy for the completion time of the real run
    chksm: str = qcloud['file']['checksum']  # is this SHA-1???
    instrmnt: str = "thermo"
        
    meta: mzqc.MetaDataParameters = mzqc.MetaDataParameters(
            inputFiles=[
                mzqc.InputFile(name=base_name,location="file:///dev/null", 
                            fileFormat=mzqc.CvParameter("MS", "MS:1000584", "mzML format"), 
                            fileProperties=[
                                mzqc.CvParameter(cvRef="MS", 
                                    accession="MS:1000747", 
                                    name="completion time", 
                                    value=cmpltn
                                ),
                                mzqc.CvParameter(cvRef="MS", 
                                    accession="MS:1000569", 
                                    name="SHA-1", 
                                    value=chksm
                                ),
                                mzqc.CvParameter(cvRef="MS", 
                                    accession="MS:1000031", 
                                    name="instrument model", 
                                    value=instrmnt
                                )
                            ]
                )
            ], 
            analysisSoftware=[
                mzqc.AnalysisSoftware(cvRef="MS", accession="MS:1000752", name="TOPP software", version="2.4", uri="openms.de")
            ]
        )

    QC_9000001 = {"QC:0000029": "Total number of PSMs", "QC:0000031": "Total number of uniquely identified peptides", "QC:0000032": "Total number of identified proteins", "QC:0000007": "MS2 spectra count"}
    QC_9000002 = dict()
    metrics: List[mzqc.QualityMetric] = list()

    for qp in qcloud['data']:
        if qp['parameter'] in [{'qCCV': "QC:1001844"}, {'qCCV': "QC:1000014"}]:
            m = mzqc.QualityMetric()
            m.accession = ":".join(["MS", qp['parameter']['qCCV'].split(':')[1]])
            m.cvRef = "MS"
            m.name = psims[m.accession].name
            mvalue: Dict[str,List[Any]] = defaultdict(list)
            for dp in qp['values']:
                mvalue['QCPeptide'].append(dp['contextSource'])
                mvalue[m.name].append(float(dp['value']))
            m.value = mvalue
            metrics.append(m)

        if qp['parameter'] == {'qCCV': "QC:9000001"}:
            m = mzqc.QualityMetric()
            m.value = qp['values'][0]['value']
            m.cvRef = "QC"
            # m.accession = name_indexed[QC_9000001[qp['values'][0]['contextSource']]]
            m.accession = "QC:9000001"
            m.name = QC_9000001[qp['values'][0]['contextSource']]
            metrics.append(m)

        if qp['parameter'] == {'qCCV': "QC:9000002"}:
            QC_9000002[":".join(["MS", qp['values'][0]['contextSource'].split(':')[1]])] = float(qp['values'][0]['value'])
        
        if qp['parameter'] == {'qCCV': "QC:9000005"}:
            m = mzqc.QualityMetric()
            m.accession = "QC:9000005"
            m.cvRef = "QC"
            m.name = "QCloud metric 5"
            m.value = float(qp['values'][0]['value'])
            metrics.append(m)

    if len(QC_9000002) == 2:
        m = mzqc.QualityMetric()
        m.accession = "QC:9000002"
        m.cvRef = "QC"
        m.name = "QCloud calibration metric 2"
        m.value = QC_9000002
        metrics.append(m)

    cv1 = mzqc.ControlledVocabulary(ref="QC", name="PSI-QC", uri="https://raw.githubusercontent.com/HUPO-PSI/mzQC/master/cv/qc-cv.obo")
    cv2 = mzqc.ControlledVocabulary(ref="MS", name="PSI-MS", uri="https://raw.githubusercontent.com/HUPO-PSI/psi-ms-CV/master/psi-ms.obo")
    rq = mzqc.RunQuality(metadata=meta, qualityMetrics=metrics)

    oqc = mzqc.MzQcFile(version="0_0_11", runQualities=[rq], controlledVocabularies=[cv1,cv2])

    mzq_m = mzqc.JsonSerialisable().ToJson(oqc, readability=1)
    with open(output, "w") as f:
        f.write("{ \"mzQC\": " + mzq_m + " }")

if __name__ == '__main__':
    convert_to_mzqc()