"""Tests for the FERC Form 1 output functions."""

import json
import logging
from contextlib import nullcontext as does_not_raise

import numpy as np
import pandas as pd
import pytest

from pudl.output.ferc1 import XbrlCalculationTreeFerc1

logger = logging.getLogger(__name__)

EXPLODED_META_IDX = ["table_name", "xbrl_factoid"]
TEST_CALC_1 = [
    {"name": "reported_1", "weight": 1.0, "source_tables": ["table_1"]},
    {"name": "reported_2", "weight": -1.0, "source_tables": ["table_1"]},
]

TEST_CALC_2 = [
    {"name": "reported_1", "weight": 1.0, "source_tables": ["table_1", "table_2"]},
    {"name": "reported_2", "weight": -1.0, "source_tables": ["table_1"]},
]

TEST_CALC_3 = [
    {"name": "reported_1", "weight": 1.0, "source_tables": ["table_1"]},
    {"name": "reported_3", "weight": 1.0, "source_tables": ["table_3"]},
]

LEAF_NODE_1 = XbrlCalculationTreeFerc1(
    **{
        "xbrl_factoid": "reported_1",
        "source_table": "table_1",
        "xbrl_factoid_original": "reported_original_1",
        "weight": 1.0,
        "children": [],
    }
)
LEAF_NODE_2 = XbrlCalculationTreeFerc1(
    **{
        "xbrl_factoid": "reported_2",
        "source_table": "table_1",
        "xbrl_factoid_original": "reported_original_2",
        "weight": -1.0,
        "children": [],
    }
)
CALC_TREE_1 = XbrlCalculationTreeFerc1(
    **{
        "xbrl_factoid": "calc_1",
        "source_table": "table_1",
        "xbrl_factoid_original": "calc_original_1",
        "weight": 1.0,
        "children": [LEAF_NODE_1, LEAF_NODE_2],
    }
)
CALC_TREE_2 = XbrlCalculationTreeFerc1(
    **{
        "xbrl_factoid": "calc_2",
        "source_table": "table_2",
        "xbrl_factoid_original": "calc_original_2",
        "weight": np.nan,
        "children": [LEAF_NODE_1, LEAF_NODE_2],
    }
)

TEST_EXPLODED_META: pd.DataFrame = (
    pd.DataFrame(
        columns=["table_name", "xbrl_factoid", "calculations", "xbrl_factoid_original"],
        data=[
            ("table_1", "reported_1", "[]", "reported_original_1"),
            ("table_1", "reported_2", "[]", "reported_original_2"),
            ("table_1", "calc_1", json.dumps(TEST_CALC_1), "calc_original_1"),
            ("table_2", "calc_2", json.dumps(TEST_CALC_2), "calc_original_2"),
            ("table_1", "calc_3", json.dumps(TEST_CALC_3), "calc_original_3"),
        ],
    )
    .convert_dtypes()
    .set_index(EXPLODED_META_IDX)
)


@pytest.mark.parametrize(
    "source_table,xbrl_factoid,weight,expected_tree,expectation",
    [
        pytest.param("table_1", "reported_1", 1.0, LEAF_NODE_1, does_not_raise()),
        pytest.param("table_1", "reported_2", -1.0, LEAF_NODE_2, does_not_raise()),
        pytest.param("table_1", "calc_1", 1.0, CALC_TREE_1, does_not_raise()),
        pytest.param(
            "table_2", "calc_2", np.nan, CALC_TREE_2, pytest.raises(AssertionError)
        ),
        pytest.param("table_1", "calc_3", np.nan, CALC_TREE_1, pytest.raises(KeyError)),
    ],
)
def test_calculation_tree_from_exploded_meta(
    source_table: str,
    xbrl_factoid: str,
    expected_tree: XbrlCalculationTreeFerc1,
    weight: float,
    expectation,
):
    """Test creation of various calculation trees."""
    with expectation:
        calc_tree = XbrlCalculationTreeFerc1.from_exploded_meta(
            source_table=source_table,
            xbrl_factoid=xbrl_factoid,
            weight=weight,
            exploded_meta=TEST_EXPLODED_META,
        )
        logger.debug(json.dumps(calc_tree.dict(), indent=4))
        assert calc_tree == expected_tree
