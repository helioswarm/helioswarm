"""Main HelioSwarm package"""

import datetime
import os
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

    Returns
    -------
    str
        Full path to the skeleton CDF
    """
    global_attrs = {
        "Acknowledgement": ["Cite Klein et al (2023)."],
        "Data_type": ["L2-summary>Level 2 summary parameters"],
        "Data_version": ["0.2.0"],
        "Descriptor": ["HSC>HelioSwarm Concept"],
        "Discipline": [
            "Space Physics>Interplanetary Studies",
            "Solar Physics>Heliospheric Physics",
        ],
        "File_naming_convention": ["source_descriptor_datatype"],
        "Generated_by": ["Jonathan Niehof"],
        "Generation_date": ["20241009"],
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
        "Logical_file_id": ["hsconcept_l2-summary_00000000_v0.2.0"],
        "Logical_source": ["hsconcept_l2-summary"],
        "Logical_source_description": ["HelioSwarm Concept Level 2 Summary"],
        "MODS": [],
        "Mission_group": ["HelioSwarm"],
        "PI_affiliation": ["University of New Hampshire"],
        "PI_name": ["Harlan Spence"],
        "Project": ["MIDEX>Medium-Class Explorers"],
        "Rules_of_use": [
            "Licensed under CC0.",
            "Cite doi:10.5281/zenodo.13887062.",
            "Redistribution is discouraged.",
        ],
        "Skeleton_version": ["0.2.0"],
        "Software_version": ["0.2.0"],
        "Source_name": ["HSC>HelioSwarm Concept"],
        "TEXT": [
            "Summary data, including Observatory configuration, for"
            " HelioSwarm representative trajectories.",
            "Phase B Swarm Reference Design 5B, Flight System Transfer Trajectory 0x75b, 2024-06-24",
        ],
        "Time_resolution": ["1 hour"],
        "TITLE": ["HelioSwarm Concept Summary"],
    }
    variables = {
        "Baseline": {
            "attrs": {
                "CATDESC": "Relative baselines",
                "DEPEND_0": "Epoch",
                "DEPEND_1": "Spacecraft_Number",
                "DEPEND_2": "Spacecraft_Number",
                "DEPEND_3": "Cartesian_Number",
                "DICT_KEY": "position",
                "DISPLAY_TYPE": "time_series",
                "FIELDNAM": "Baseline",
                "LABLAXIS": "Baseline",
                "LABL_PTR_1": "Spacecraft_Label",
                "LABL_PTR_2": "Spacecraft_Label",
                "LABL_PTR_3": "Cartesian_Label",
                "SCALEMAX": 2500,
                "SCALEMIN": -2500,
                "UNITS": "km",
                "VALIDMAX": 15000,
                "VALIDMIN": -15000,
                "VAR_NOTES": "Directed vector from first index to second index, e.g. [3, 4, 1] is"
                " Y component of vector pointing from N3 to N4.",
                "VAR_TYPE": "data",
            },
            "compress": spacepy.pycdf.const.GZIP_COMPRESSION,
            "compress_param": 7,
            "dims": (9, 9, 3),
            "type": spacepy.pycdf.const.CDF_REAL8,
        },
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
                "SCALEMIN": -383000,
                "UNITS": "km",
                "VALIDMAX": 520000,  # 80Re after first lunar swingby
                "VALIDMIN": -520000,
                "VAR_TYPE": "data",
            },
            "compress": spacepy.pycdf.const.GZIP_COMPRESSION,
            "compress_param": 7,
            "dims": (9, 3),
            "type": spacepy.pycdf.const.CDF_REAL8,
        },
        "Spacecraft_Label": {
            "data": spacepy.dmarray(
                ["H"] + [f"N{i}" for i in range(1, 9)],
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
                list(range(9)),
                dtype=numpy.int8,
                attrs={
                    "CATDESC": "Spacecraft number",
                    "DICT_KEY": "number",
                    "FIELDNAM": "Spacecraft number",
                    "LABLAXIS": "S/C",
                    "SCALEMAX": 9,
                    "SCALEMIN": -1,
                    "VALIDMAX": 8,
                    "VALIDMIN": 0,
                    "VAR_NOTES": "Hub 0, nodes 1-8.",
                    "VAR_TYPE": "support_data",
                },
            ),
            "recVary": False,
        },
        "True_Anomaly": {
            "attrs": {
                "CATDESC": "True anomaly",
                "DEPEND_0": "Epoch",
                "DEPEND_1": "Spacecraft_Number",
                "DICT_KEY": "angle>rotation",
                "DISPLAY_TYPE": "time_series",
                "FIELDNAM": "True anomaly",
                "LABLAXIS": "f",
                "LABL_PTR_1": "Spacecraft_Label",
                "SCALEMAX": 360,
                "SCALEMIN": -0,
                "UNITS": "degrees",
                "VALIDMAX": 360,
                "VALIDMIN": 0,
                "VAR_TYPE": "data",
            },
            "compress": spacepy.pycdf.const.GZIP_COMPRESSION,
            "compress_param": 7,
            "dims": (9,),
            "type": spacepy.pycdf.const.CDF_REAL4,
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


def read_positions(directory):
    """Read all representative trajectory position files

    Parameters
    ----------
    directory : str
        Directory containing representative trajectory position files

    Returns
    -------
    tuple
        `ndarray` of times,  `ndarray` of positions (time, 9, 3), `ndarray`
        of true anomaly (degrees) (time, 9). Hub first.
    """
    dates, positions, true_anom = [], [], []
    for i in range(9):
        fname = f"Node{i}_preProcessed.txt" if i else "Chief.txt"
        with open(os.path.join(directory, fname), "rb") as f:  # binary so tell() works
            l = b""
            while not l.startswith(b"------"):  # Scan past header
                l = next(f)
            # Underlining is not same width as field, start field at end of previous underline
            colstart = [j for j in range(len(l)) if j == 0 or l[j - 1] == 45 and l[j] == 32] + [
                len(l.rstrip())
            ]
            widths = [colstart[i + 1] - colstart[i] for i in range(len(colstart) - 1)]
            pos = f.tell()
            # This is NOT PORTABLE across locales, %b is locale-dependent
            dates.append(
                numpy.genfromtxt(
                    f,
                    delimiter=widths,
                    converters={
                        0: lambda x: datetime.datetime.strptime(
                            x.decode("ascii"), "%d %b %Y %H:%M:%S.%f"
                        )
                    },
                    dtype=object,
                    usecols=(0,),
                )
            )
            f.seek(pos, os.SEEK_SET)
            positions.append(numpy.genfromtxt(f, delimiter=widths, usecols=(1, 2, 3)))
            f.seek(pos, os.SEEK_SET)
            true_anom.append(numpy.genfromtxt(f, delimiter=widths, usecols=(5,)))
    for i in range(1, 9):
        if (dates[i] != dates[0]).any():
            raise ValueError(f"N{i} dates do not match hub.")
    pos_out = numpy.stack(positions, axis=1)
    true_anom = numpy.stack(true_anom, axis=1)
    return dates[0], pos_out, true_anom


def write_summary(in_directory, out_directory):
    """Write CDFs of the summary file

    Parameters
    ----------
    in_directory : str
        Directory containing the representative trajectory input files
    out_directory : str
        Directory to hold the output files
    """
    skeleton = make_summary_skeleton(out_directory)
    dates, positions, true_anom = read_positions(in_directory)
    # Vector points from first index to second index
    head = numpy.repeat(positions, 9, axis=0).reshape(-1, 9, 9, 3)
    tail = numpy.repeat(positions, 9, axis=1).reshape(-1, 9, 9, 3)
    baselines = head - tail
    yyyymm = numpy.vectorize(lambda x: x.year * 100 + x.month)(dates)
    starts = numpy.concatenate(([0], numpy.nonzero(numpy.diff(yyyymm))[0] + 1))
    stops = numpy.concatenate((starts[1:], [yyyymm.shape[0]]))
    for start, stop in zip(starts, stops):
        logical_fileid = f"hsconcept_l2-summary_{yyyymm[start]}01_v0.2.0"
        outcdf = os.path.join(out_directory, f"{logical_fileid}.cdf")
        with spacepy.pycdf.CDF(outcdf, skeleton) as f:
            f.attrs["Logical_file_id"] = [logical_fileid]
            f["Epoch"][...] = dates[start:stop]
            f["Position"][...] = positions[start:stop, ...]
            f["Baseline"][...] = baselines[start:stop, ...]
            f["True_Anomaly"][...] = true_anom[start:stop, ...]
