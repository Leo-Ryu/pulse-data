# Recidiviz - a data platform for criminal justice reform
# Copyright (C) 2019 Recidiviz, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# =============================================================================
from unittest import TestCase

import attr

from recidiviz.persistence.entity.state.entities import StatePersonExternalId, \
    StatePerson, StatePersonAlias, StateCharge, StateSentenceGroup, StateFine
from recidiviz.persistence.entity_matching.state.state_matching_utils import \
    is_match, merge_flat_fields, remove_back_edges, add_person_to_entity_graph

_EXTERNAL_ID = 'EXTERNAL_ID' \
               ''
_EXTERNAL_ID_2 = 'EXTERNAL_ID_2'
_EXTERNAL_ID_3 = 'EXTERNAL_ID_3'
_ID = 1
_ID_2 = 2
_ID_3 = 3
_STATE_CODE = 'NC'
_STATE_CODE_ANOTHER = 'CA'
_FULL_NAME = 'NAME'


class TestStateMatchingUtils(TestCase):
    """Tests for state entity matching utils"""

    def test_isMatch_StatePerson(self):
        external_id = StatePersonExternalId.new_with_defaults(
            state_code=_STATE_CODE, external_id=_EXTERNAL_ID)
        external_id_different = attr.evolve(
            external_id, external_id=_EXTERNAL_ID_2)
        person = StatePerson.new_with_defaults(
            full_name='name', external_ids=[external_id])
        person_another = StatePerson.new_with_defaults(
            full_name='name_2', external_ids=[external_id])

        self.assertTrue(
            is_match(ingested_entity=person, db_entity=person_another))
        person_another.external_ids = [external_id_different]
        self.assertFalse(
            is_match(ingested_entity=person, db_entity=person_another))

    def test_isMatch_StatePersonExternalId(self):
        external_id = StatePersonExternalId.new_with_defaults(
            state_code=_STATE_CODE, id_type='type', external_id=_EXTERNAL_ID)
        external_id_different = attr.evolve(external_id, id_type='type_2')
        self.assertTrue(is_match(ingested_entity=external_id,
                                 db_entity=external_id_different))
        external_id_different.external_id = _EXTERNAL_ID_2
        self.assertFalse(is_match(ingested_entity=external_id,
                                  db_entity=external_id_different))

    def test_isMatch_StatePersonAlias(self):
        alias = StatePersonAlias.new_with_defaults(
            state_code=_STATE_CODE, full_name='full_name')
        alias_another = attr.evolve(alias, full_name='full_name_2')
        self.assertTrue(
            is_match(ingested_entity=alias, db_entity=alias_another))
        alias_another.state_code = _STATE_CODE_ANOTHER
        self.assertFalse(
            is_match(ingested_entity=alias, db_entity=alias_another))

    def test_isMatch_defaultCompareExternalId(self):
        charge = StateCharge.new_with_defaults(
            external_id=_EXTERNAL_ID, description='description')
        charge_another = attr.evolve(charge, description='description_another')
        self.assertTrue(
            is_match(ingested_entity=charge, db_entity=charge_another))
        charge.external_id = _EXTERNAL_ID_2
        self.assertFalse(
            is_match(ingested_entity=charge, db_entity=charge_another))

    def test_mergeFlatFields(self):
        ing_entity = StateSentenceGroup.new_with_defaults(
            county_code='county_code-updated', max_length_days=10)
        db_entity = StateSentenceGroup.new_with_defaults(
            sentence_group_id=_ID, county_code='county_code')
        expected_entity = attr.evolve(ing_entity, sentence_group_id=_ID)

        self.assertEqual(
            expected_entity,
            merge_flat_fields(ingested_entity=ing_entity, db_entity=db_entity))

    def test_removeBackedges(self):
        person = StatePerson.new_with_defaults(full_name=_FULL_NAME)
        sentence_group = StateSentenceGroup.new_with_defaults(
            external_id=_EXTERNAL_ID, person=person)
        fine = StateFine.new_with_defaults(
            external_id=_EXTERNAL_ID,
            sentence_group=sentence_group, person=person)

        sentence_group.fines = [fine]
        person.sentence_groups = [sentence_group]

        expected_fine = attr.evolve(
            fine, sentence_group=None, person=None)
        expected_sentence_group = attr.evolve(
            sentence_group, person=None, fines=[expected_fine])
        expected_person = attr.evolve(
            person, sentence_groups=[expected_sentence_group])

        remove_back_edges(person)
        self.assertEqual(expected_person, person)

    def test_addPersonToEntityTree(self):
        fine = StateFine.new_with_defaults(external_id=_EXTERNAL_ID)
        sentence_group = StateSentenceGroup.new_with_defaults(
            external_id=_EXTERNAL_ID,
            fines=[fine])
        person = StatePerson.new_with_defaults(
            full_name=_FULL_NAME,
            sentence_groups=[sentence_group])

        expected_person = attr.evolve(person)
        expected_fine = attr.evolve(fine, person=expected_person)
        expected_sentence_group = attr.evolve(
            sentence_group, person=expected_person, fines=[expected_fine])
        expected_person.sentence_groups = [expected_sentence_group]

        add_person_to_entity_graph([person])
        self.assertEqual(expected_person, person)
