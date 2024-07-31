"""Main HelioSwarm package"""

import datetime
import os.path

import numpy
import spacepy
import spacepy.pycdf
import spacepy.pycdf.const
import spacepy.pycdf.istp


def make_summary_skeleton(outdir="."):
    """Create skeleton CDF for the summary data (positions, baselines)

    Parameters
    ----------
    outdir : str
        Path to directory to hold skeleton CDF
    """
    global_attrs = {
        "Acknowledgement": ["Cite Klein et al (2023)."],
        "Data_type": ["L2-summary>Level 2 summary parameters"],
        "Data_version": ["0.0.0"],
        "Descriptor": ["HSC>HelioSwarm Concept"],
        "Discipline": [
            "Space Physics>Interplanetary Studies",
            "Solar Physics>Heliospheric Physics",
        ],
        "File_naming_convention": ["source_descriptor_datatype"],
        "Generated_by": ["Jonathan Niehof"],
        "Generation_date": ["20240730"],
        "HTTP_LINK": [
            "https://link.springer.com/article/10.1007/s11214-023-01019-0",
            "https://zenodo.org/doi/10.5281/zenodo.3252523",
            "https://github.com/helioswarm",
        ],
        "Instrument_type": [
            "Ephemeris",
            "Magnetic Fields (Space)",
            "Plasma and Solar Wind",
        ],
        "LINK_TEXT": [
            "Mission paper at ",
            "Generated with ",
            "Documentation and HelioSwarm code are on ",
        ],
        "LINK_TITLE": [
            "SSR.",
            "spacepy.",
            "GitHub.",
        ],
        "Logical_file_id": ["hsconcept_l2-summary_00000000_v0.0.0"],
        "Logical_source": ["hsconcept_l2-summary"],
        "Logical_source_description": ["HelioSwarm Concept Level 2 Summary"],
        "MODS": [],
        "Mission_group": ["HelioSwarm"],
        "PI_affiliation": ["University of New Hampshire"],
        "PI_name": ["Harlan Spence"],
        "Project": ["MIDEX>Medium-Class Explorers"],
        #        'Rules_of_use': [],
        "Skeleton_version": ["0.0.0"],
        "Software_version": ["0.0.0"],
        "Source_name": ["HSC>HelioSwarm Concept"],
        "TEXT": [
            "Summary data, including Observatory configuration, for"
            " the HelioSwarm Phase B concept Design Reference Mission."
        ],
        "Time_resolution": ["1 hour"],
        "TITLE": ["HelioSwarm Concept Summary"],
    }
    variables = {
        "Cartesian_Label": {
            "data": spacepy.dmarray(
                ["X", "Y", "Z"],
                attrs={
                    "CATDESC": "Label for Cartesian XYZ dimensions",
                    "DICT_KEY": "label",
                    "FIELDNAM": "Cartesian label",
                    "VAR_TYPE": "metadata",
                },
            ),
            "recVary": False,
        },
        "Cartesian_Number": {
            "data": spacepy.dmarray(
                numpy.arange(3, dtype=numpy.int8),
                attrs={
                    "CATDESC": "Axis number for Cartesian XYZ dimensions",
                    "DICT_KEY": "number",
                    "FIELDNAM": "Axis number",
                    "LABLAXIS": "Axis",
                    "SCALEMAX": 4,
                    "SCALEMIN": -1,
                    "VALIDMAX": 2,
                    "VALIDMIN": 0,
                    "VAR_TYPE": "support_data",
                },
            ),
            "recVary": False,
        },
        "Epoch": {
            "attrs": {
                "CATDESC": "Default time",
                "DICT_KEY": "time>epoch",
                "FIELDNAM": "Epoch",
                "LABLAXIS": "Time",
                "MONOTON": "INCREASE",
                "SCALEMIN": datetime.datetime(2025, 1, 1),
                "SCALEMAX": datetime.datetime(2035, 1, 1),
                "SCALETYP": "linear",
                "UNITS": "UTC",
                "VALIDMAX": datetime.datetime(2099, 12, 31, 23, 59, 59, 999000),
                "VALIDMIN": datetime.datetime(1990, 1, 1, 0, 0),
                "VAR_NOTES": "Point-in-time measurement.",
                "VAR_TYPE": "support_data",
            },
            "type": spacepy.pycdf.const.CDF_TIME_TT2000,
        },
        "Position": {
            "attrs": {
                "CATDESC": "Spacecraft position",
                "DEPEND_0": "Epoch",
                "DEPEND_1": "Spacecraft_Number",
                "DEPEND_2": "Cartesian_Number",
                "DICT_KEY": "position",
                "DISPLAY_TYPE": "time_series",
                "FIELDNAM": "Position",
                "LABLAXIS": "GSE Pos",
                "LABL_PTR_1": "Spacecraft_Label",
                "LABL_PTR_2": "Cartesian_Label",
                "SCALEMAX": 383000,  # 60 Re apogee sci orbit
                "SCALEMIN": 105000,  # 17 Re perigee sci orbit
                "UNITS": "km",
                "VALIDMAX": 520000,  # 80Re after first lunar swingby
                "VALIDMIN": 6000,  # above ground
                "VAR_TYPE": "data",
            },
            "dims": (10, 3),
            "type": spacepy.pycdf.const.CDF_REAL4,
        },
        "Spacecraft_Label": {
            "data": spacepy.dmarray(
                ["N/A"] + [f"N{i}" for i in range(1, 9)] + ["H"],
                attrs={
                    "CATDESC": "Spacecraft label",
                    "DICT_KEY": "label",
                    "FIELDNAM": "Spacecraft label",
                    "VAR_TYPE": "metadata",
                },
            ),
            "recVary": False,
        },
        "Spacecraft_Number": {
            "data": spacepy.dmarray(
                [-128] + list(range(1, 10)),
                dtype=numpy.int8,
                attrs={
                    "CATDESC": "Spacecraft number",
                    "DICT_KEY": "number",
                    "FIELDNAM": "Spacecraft number",
                    "LABLAXIS": "S/C",
                    "SCALEMAX": 10,
                    "SCALEMIN": 0,
                    "VALIDMAX": 9,
                    "VALIDMIN": 1,
                    "VAR_NOTES": "Nodes 1-8, hub 9, no s/c 0",
                    "VAR_TYPE": "support_data",
                },
            ),
            "recVary": False,
        },
    }
    ver = global_attrs["Skeleton_version"][0]
    fspec = os.path.join(outdir, global_attrs["Logical_source"][0] + "_00000000_v" + ver + ".cdf")
    with spacepy.pycdf.CDF(fspec, create=True) as cdf:
        cdf.attrs = global_attrs
        for name, kwargs in variables.items():
            a = kwargs.get("attrs")
            if a is not None:
                del kwargs["attrs"]
            v = cdf.new(name, **kwargs)
            spacepy.pycdf.istp.fillval(v)
            spacepy.pycdf.istp.format(v)
            if a is not None:
                v.attrs.update(a)
    return fspec
