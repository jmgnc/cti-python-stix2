import datetime as dt

import pytest
import pytz

import stix2

from .constants import (
    FAKE_TIME, INDICATOR_ID, MALWARE_ID, RELATIONSHIP_ID, RELATIONSHIP_KWARGS,
)

EXPECTED_RELATIONSHIP = """{
    "type": "relationship",
    "spec_version": "2.1",
    "id": "relationship--df7c87eb-75d2-4948-af81-9d49d246f301",
    "created": "2016-04-06T20:06:37.000Z",
    "modified": "2016-04-06T20:06:37.000Z",
    "relationship_type": "indicates",
    "source_ref": "indicator--a740531e-63ff-4e49-a9e1-a0a3eed0e3e7",
    "target_ref": "malware--9c4638ec-f1de-4ddb-abf4-1b760417654e"
}"""


def test_relationship_all_required_properties():
    now = dt.datetime(2016, 4, 6, 20, 6, 37, tzinfo=pytz.utc)

    rel = stix2.v21.Relationship(
        type='relationship',
        id=RELATIONSHIP_ID,
        created=now,
        modified=now,
        relationship_type='indicates',
        source_ref=INDICATOR_ID,
        target_ref=MALWARE_ID,
    )
    assert str(rel) == EXPECTED_RELATIONSHIP


def test_relationship_autogenerated_properties(relationship):
    assert relationship.type == 'relationship'
    assert relationship.spec_version == '2.1'
    assert relationship.id == 'relationship--00000000-0000-4000-8000-000000000001'
    assert relationship.created == FAKE_TIME
    assert relationship.modified == FAKE_TIME
    assert relationship.relationship_type == 'indicates'
    assert relationship.source_ref == INDICATOR_ID
    assert relationship.target_ref == MALWARE_ID

    assert relationship['type'] == 'relationship'
    assert relationship['spec_version'] == '2.1'
    assert relationship['id'] == 'relationship--00000000-0000-4000-8000-000000000001'
    assert relationship['created'] == FAKE_TIME
    assert relationship['modified'] == FAKE_TIME
    assert relationship['relationship_type'] == 'indicates'
    assert relationship['source_ref'] == INDICATOR_ID
    assert relationship['target_ref'] == MALWARE_ID


def test_relationship_type_must_be_relationship():
    with pytest.raises(stix2.exceptions.InvalidValueError) as excinfo:
        stix2.v21.Relationship(type='xxx', **RELATIONSHIP_KWARGS)

    assert excinfo.value.cls == stix2.v21.Relationship
    assert excinfo.value.prop_name == "type"
    assert excinfo.value.reason == "must equal 'relationship'."
    assert str(excinfo.value) == "Invalid value for Relationship 'type': must equal 'relationship'."


def test_relationship_id_must_start_with_relationship():
    with pytest.raises(stix2.exceptions.InvalidValueError) as excinfo:
        stix2.v21.Relationship(id='my-prefix--', **RELATIONSHIP_KWARGS)

    assert excinfo.value.cls == stix2.v21.Relationship
    assert excinfo.value.prop_name == "id"
    assert excinfo.value.reason == "must start with 'relationship--'."
    assert str(excinfo.value) == "Invalid value for Relationship 'id': must start with 'relationship--'."


def test_relationship_required_property_relationship_type():
    with pytest.raises(stix2.exceptions.MissingPropertiesError) as excinfo:
        stix2.v21.Relationship()
    assert excinfo.value.cls == stix2.v21.Relationship
    assert excinfo.value.properties == ["relationship_type", "source_ref", "target_ref"]


def test_relationship_missing_some_required_properties():
    with pytest.raises(stix2.exceptions.MissingPropertiesError) as excinfo:
        stix2.v21.Relationship(relationship_type='indicates')

    assert excinfo.value.cls == stix2.v21.Relationship
    assert excinfo.value.properties == ["source_ref", "target_ref"]


def test_relationship_required_properties_target_ref():
    with pytest.raises(stix2.exceptions.MissingPropertiesError) as excinfo:
        stix2.v21.Relationship(
            relationship_type='indicates',
            source_ref=INDICATOR_ID,
        )

    assert excinfo.value.cls == stix2.v21.Relationship
    assert excinfo.value.properties == ["target_ref"]


def test_cannot_assign_to_relationship_attributes(relationship):
    with pytest.raises(stix2.exceptions.ImmutableError) as excinfo:
        relationship.relationship_type = "derived-from"

    assert str(excinfo.value) == "Cannot modify 'relationship_type' property in 'Relationship' after creation."


def test_invalid_kwarg_to_relationship():
    with pytest.raises(stix2.exceptions.ExtraPropertiesError) as excinfo:
        stix2.v21.Relationship(my_custom_property="foo", **RELATIONSHIP_KWARGS)

    assert excinfo.value.cls == stix2.v21.Relationship
    assert excinfo.value.properties == ['my_custom_property']
    assert str(excinfo.value) == "Unexpected properties for Relationship: (my_custom_property)."


def test_create_relationship_from_objects_rather_than_ids1(indicator, malware):
    rel = stix2.v21.Relationship(
        relationship_type="indicates",
        source_ref=indicator,
        target_ref=malware,
        stop_time="2016-04-06T20:03:48Z",
    )

    assert rel.relationship_type == 'indicates'
    assert rel.source_ref == 'indicator--00000000-0000-4000-8000-000000000001'
    assert rel.target_ref == 'malware--00000000-0000-4000-8000-000000000003'
    assert rel.id == 'relationship--00000000-0000-4000-8000-000000000005'
    assert rel.stop_time == dt.datetime(2016, 4, 6, 20, 3, 48, tzinfo=pytz.utc)


def test_create_relationship_from_objects_rather_than_ids2(indicator, malware):
    rel = stix2.v21.Relationship(
        relationship_type="indicates",
        source_ref=indicator,
        target_ref=malware,
        start_time="2016-04-06T20:03:48Z",
    )

    assert rel.relationship_type == 'indicates'
    assert rel.source_ref == 'indicator--00000000-0000-4000-8000-000000000001'
    assert rel.target_ref == 'malware--00000000-0000-4000-8000-000000000003'
    assert rel.id == 'relationship--00000000-0000-4000-8000-000000000005'
    assert rel.start_time == dt.datetime(2016, 4, 6, 20, 3, 48, tzinfo=pytz.utc)


def test_create_relationship_with_positional_args(indicator, malware):
    rel = stix2.v21.Relationship(indicator, 'indicates', malware)

    assert rel.relationship_type == 'indicates'
    assert rel.source_ref == 'indicator--00000000-0000-4000-8000-000000000001'
    assert rel.target_ref == 'malware--00000000-0000-4000-8000-000000000003'
    assert rel.id == 'relationship--00000000-0000-4000-8000-000000000005'


@pytest.mark.parametrize(
    "data", [
        EXPECTED_RELATIONSHIP,
        {
            "created": "2016-04-06T20:06:37Z",
            "id": RELATIONSHIP_ID,
            "modified": "2016-04-06T20:06:37Z",
            "relationship_type": "indicates",
            "source_ref": INDICATOR_ID,
            "target_ref": MALWARE_ID,
            "spec_version": "2.1",
            "type": "relationship",
        },
    ],
)
def test_parse_relationship(data):
    rel = stix2.parse(data, version="2.1")

    assert rel.type == 'relationship'
    assert rel.spec_version == '2.1'
    assert rel.id == RELATIONSHIP_ID
    assert rel.created == dt.datetime(2016, 4, 6, 20, 6, 37, tzinfo=pytz.utc)
    assert rel.modified == dt.datetime(2016, 4, 6, 20, 6, 37, tzinfo=pytz.utc)
    assert rel.relationship_type == "indicates"
    assert rel.source_ref == INDICATOR_ID
    assert rel.target_ref == MALWARE_ID


@pytest.mark.parametrize(
    "data", [
        {
            "created": "2016-04-06T20:06:37Z",
            "id": RELATIONSHIP_ID,
            "modified": "2016-04-06T20:06:37Z",
            "relationship_type": "indicates",
            "source_ref": INDICATOR_ID,
            "target_ref": MALWARE_ID,
            "start_time": "2018-04-06T20:06:37Z",
            "stop_time": "2016-04-06T20:06:37Z",
            "spec_version": "2.1",
            "type": "relationship",
        },
    ],
)
def test_parse_relationship_with_wrong_start_and_stop_time(data):
    with pytest.raises(ValueError) as excinfo:
        stix2.parse(data)

    assert str(excinfo.value) == "{id} 'stop_time' must be later than 'start_time'".format(**data)
