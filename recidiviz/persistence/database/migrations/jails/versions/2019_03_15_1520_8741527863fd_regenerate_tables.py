"""regenerate_tables

Revision ID: 8741527863fd
Revises: 4e851ca7f4f8
Create Date: 2019-03-15 15:20:46.697351

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8741527863fd'
down_revision = '4e851ca7f4f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('person',
    sa.Column('external_id', sa.String(length=255), nullable=True),
    sa.Column('gender', sa.Enum('EXTERNAL_UNKNOWN', 'FEMALE', 'MALE', 'OTHER', 'TRANS_FEMALE', 'TRANS_MALE', name='gender'), nullable=True),
    sa.Column('gender_raw_text', sa.String(length=255), nullable=True),
    sa.Column('race', sa.Enum('AMERICAN_INDIAN_ALASKAN_NATIVE', 'ASIAN', 'BLACK', 'EXTERNAL_UNKNOWN', 'NATIVE_HAWAIIAN_PACIFIC_ISLANDER', 'OTHER', 'WHITE', name='race'), nullable=True),
    sa.Column('race_raw_text', sa.String(length=255), nullable=True),
    sa.Column('ethnicity', sa.Enum('EXTERNAL_UNKNOWN', 'HISPANIC', 'NOT_HISPANIC', name='ethnicity'), nullable=True),
    sa.Column('ethnicity_raw_text', sa.String(length=255), nullable=True),
    sa.Column('residency_status', sa.Enum('HOMELESS', 'PERMANENT', 'TRANSIENT', name='residency_status'), nullable=True),
    sa.Column('resident_of_region', sa.Boolean(), nullable=True),
    sa.Column('region', sa.String(length=255), nullable=False),
    sa.Column('jurisdiction_id', sa.String(length=255), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=255), nullable=True),
    sa.Column('birthdate', sa.Date(), nullable=True),
    sa.Column('birthdate_inferred_from_age', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('person_id')
    )
    op.create_index(op.f('ix_person_birthdate'), 'person', ['birthdate'], unique=False)
    op.create_index(op.f('ix_person_external_id'), 'person', ['external_id'], unique=False)
    op.create_index(op.f('ix_person_full_name'), 'person', ['full_name'], unique=False)
    op.create_index(op.f('ix_person_region'), 'person', ['region'], unique=False)
    op.create_table('booking',
    sa.Column('external_id', sa.String(length=255), nullable=True),
    sa.Column('admission_date', sa.Date(), nullable=True),
    sa.Column('admission_reason', sa.Enum('ESCAPE', 'NEW_COMMITMENT', 'PAROLE_VIOLATION', 'PROBATION_VIOLATION', 'TRANSFER', name='admission_reason'), nullable=True),
    sa.Column('admission_reason_raw_text', sa.String(length=255), nullable=True),
    sa.Column('admission_date_inferred', sa.Boolean(), nullable=True),
    sa.Column('release_date', sa.Date(), nullable=True),
    sa.Column('release_date_inferred', sa.Boolean(), nullable=True),
    sa.Column('projected_release_date', sa.Date(), nullable=True),
    sa.Column('release_reason', sa.Enum('ACQUITTAL', 'BOND', 'CASE_DISMISSED', 'DEATH', 'ESCAPE', 'EXPIRATION_OF_SENTENCE', 'EXTERNAL_UNKNOWN', 'OWN_RECOGNIZANCE', 'PAROLE', 'PROBATION', 'TRANSFER', name='release_reason'), nullable=True),
    sa.Column('release_reason_raw_text', sa.String(length=255), nullable=True),
    sa.Column('custody_status', sa.Enum('ESCAPED', 'HELD_ELSEWHERE', 'IN_CUSTODY', 'INFERRED_RELEASE', 'RELEASED', 'PRESENT_WITHOUT_INFO', 'REMOVED_WITHOUT_INFO', name='custody_status'), nullable=False),
    sa.Column('custody_status_raw_text', sa.String(length=255), nullable=True),
    sa.Column('facility', sa.String(length=255), nullable=True),
    sa.Column('classification', sa.Enum('EXTERNAL_UNKNOWN', 'HIGH', 'LOW', 'MAXIMUM', 'MEDIUM', 'MINIMUM', 'WORK_RELEASE', name='classification'), nullable=True),
    sa.Column('classification_raw_text', sa.String(length=255), nullable=True),
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.Column('last_seen_time', sa.DateTime(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['person_id'], ['person.person_id'], ),
    sa.PrimaryKeyConstraint('booking_id')
    )
    op.create_index(op.f('ix_booking_external_id'), 'booking', ['external_id'], unique=False)
    op.create_table('person_history',
    sa.Column('external_id', sa.String(length=255), nullable=True),
    sa.Column('gender', sa.Enum('EXTERNAL_UNKNOWN', 'FEMALE', 'MALE', 'OTHER', 'TRANS_FEMALE', 'TRANS_MALE', name='gender'), nullable=True),
    sa.Column('gender_raw_text', sa.String(length=255), nullable=True),
    sa.Column('race', sa.Enum('AMERICAN_INDIAN_ALASKAN_NATIVE', 'ASIAN', 'BLACK', 'EXTERNAL_UNKNOWN', 'NATIVE_HAWAIIAN_PACIFIC_ISLANDER', 'OTHER', 'WHITE', name='race'), nullable=True),
    sa.Column('race_raw_text', sa.String(length=255), nullable=True),
    sa.Column('ethnicity', sa.Enum('EXTERNAL_UNKNOWN', 'HISPANIC', 'NOT_HISPANIC', name='ethnicity'), nullable=True),
    sa.Column('ethnicity_raw_text', sa.String(length=255), nullable=True),
    sa.Column('residency_status', sa.Enum('HOMELESS', 'PERMANENT', 'TRANSIENT', name='residency_status'), nullable=True),
    sa.Column('resident_of_region', sa.Boolean(), nullable=True),
    sa.Column('region', sa.String(length=255), nullable=False),
    sa.Column('jurisdiction_id', sa.String(length=255), nullable=False),
    sa.Column('person_history_id', sa.Integer(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.Column('valid_from', sa.DateTime(), nullable=False),
    sa.Column('valid_to', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['person_id'], ['person.person_id'], ),
    sa.PrimaryKeyConstraint('person_history_id')
    )
    op.create_index(op.f('ix_person_history_external_id'), 'person_history', ['external_id'], unique=False)
    op.create_index(op.f('ix_person_history_person_id'), 'person_history', ['person_id'], unique=False)
    op.create_index(op.f('ix_person_history_region'), 'person_history', ['region'], unique=False)
    op.create_table('arrest',
    sa.Column('external_id', sa.String(length=255), nullable=True),
    sa.Column('arrest_date', sa.Date(), nullable=True),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('agency', sa.String(length=255), nullable=True),
    sa.Column('officer_name', sa.String(length=255), nullable=True),
    sa.Column('officer_id', sa.String(length=255), nullable=True),
    sa.Column('arrest_id', sa.Integer(), nullable=False),
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['booking_id'], ['booking.booking_id'], ),
    sa.PrimaryKeyConstraint('arrest_id')
    )
    op.create_index(op.f('ix_arrest_external_id'), 'arrest', ['external_id'], unique=False)
    op.create_table('bond',
    sa.Column('external_id', sa.String(length=255), nullable=True),
    sa.Column('amount_dollars', sa.Integer(), nullable=True),
    sa.Column('bond_type', sa.Enum('EXTERNAL_UNKNOWN', 'CASH', 'NO_BOND', 'PARTIAL_CASH', 'SECURED', 'REMOVED_WITHOUT_INFO', 'UNSECURED', name='bond_type'), nullable=True),
    sa.Column('bond_type_raw_text', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Enum('DENIED', 'PRESENT_WITHOUT_INFO', 'INFERRED_SET', 'NOT_REQUIRED', 'PENDING', 'POSTED', 'REVOKED', 'REMOVED_WITHOUT_INFO', 'SET', name='bond_status'), nullable=False),
    sa.Column('status_raw_text', sa.String(length=255), nullable=True),
    sa.Column('bond_agent', sa.String(length=255), nullable=True),
    sa.Column('bond_id', sa.Integer(), nullable=False),
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['booking_id'], ['booking.booking_id'], initially='DEFERRED', deferrable=True),
    sa.PrimaryKeyConstraint('bond_id')
    )
    op.create_index(op.f('ix_bond_external_id'), 'bond', ['external_id'], unique=False)
    op.create_table('booking_history',
    sa.Column('external_id', sa.String(length=255), nullable=True),
    sa.Column('admission_date', sa.Date(), nullable=True),
    sa.Column('admission_reason', sa.Enum('ESCAPE', 'NEW_COMMITMENT', 'PAROLE_VIOLATION', 'PROBATION_VIOLATION', 'TRANSFER', name='admission_reason'), nullable=True),
    sa.Column('admission_reason_raw_text', sa.String(length=255), nullable=True),
    sa.Column('admission_date_inferred', sa.Boolean(), nullable=True),
    sa.Column('release_date', sa.Date(), nullable=True),
    sa.Column('release_date_inferred', sa.Boolean(), nullable=True),
    sa.Column('projected_release_date', sa.Date(), nullable=True),
    sa.Column('release_reason', sa.Enum('ACQUITTAL', 'BOND', 'CASE_DISMISSED', 'DEATH', 'ESCAPE', 'EXPIRATION_OF_SENTENCE', 'EXTERNAL_UNKNOWN', 'OWN_RECOGNIZANCE', 'PAROLE', 'PROBATION', 'TRANSFER', name='release_reason'), nullable=True),
    sa.Column('release_reason_raw_text', sa.String(length=255), nullable=True),
    sa.Column('custody_status', sa.Enum('ESCAPED', 'HELD_ELSEWHERE', 'IN_CUSTODY', 'INFERRED_RELEASE', 'RELEASED', 'PRESENT_WITHOUT_INFO', 'REMOVED_WITHOUT_INFO', name='custody_status'), nullable=False),
    sa.Column('custody_status_raw_text', sa.String(length=255), nullable=True),
    sa.Column('facility', sa.String(length=255), nullable=True),
    sa.Column('classification', sa.Enum('EXTERNAL_UNKNOWN', 'HIGH', 'LOW', 'MAXIMUM', 'MEDIUM', 'MINIMUM', 'WORK_RELEASE', name='classification'), nullable=True),
    sa.Column('classification_raw_text', sa.String(length=255), nullable=True),
    sa.Column('booking_history_id', sa.Integer(), nullable=False),
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.Column('valid_from', sa.DateTime(), nullable=False),
    sa.Column('valid_to', sa.DateTime(), nullable=True),
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['booking_id'], ['booking.booking_id'], ),
    sa.ForeignKeyConstraint(['person_id'], ['person.person_id'], ),
    sa.PrimaryKeyConstraint('booking_history_id')
    )
    op.create_index(op.f('ix_booking_history_booking_id'), 'booking_history', ['booking_id'], unique=False)
    op.create_index(op.f('ix_booking_history_external_id'), 'booking_history', ['external_id'], unique=False)
    op.create_table('hold',
    sa.Column('external_id', sa.String(length=255), nullable=True),
    sa.Column('jurisdiction_name', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Enum('ACTIVE', 'INACTIVE', 'INFERRED_DROPPED', 'PRESENT_WITHOUT_INFO', 'REMOVED_WITHOUT_INFO', name='hold_status'), nullable=False),
    sa.Column('status_raw_text', sa.String(length=255), nullable=True),
    sa.Column('hold_id', sa.Integer(), nullable=False),
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['booking_id'], ['booking.booking_id'], ),
    sa.PrimaryKeyConstraint('hold_id')
    )
    op.create_index(op.f('ix_hold_external_id'), 'hold', ['external_id'], unique=False)
    op.create_table('sentence',
    sa.Column('external_id', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Enum('COMMUTED', 'COMPLETED', 'SERVING', 'PRESENT_WITHOUT_INFO', 'REMOVED_WITHOUT_INFO', name='sentence_status'), nullable=False),
    sa.Column('status_raw_text', sa.String(length=255), nullable=True),
    sa.Column('sentencing_region', sa.String(length=255), nullable=True),
    sa.Column('min_length_days', sa.Integer(), nullable=True),
    sa.Column('max_length_days', sa.Integer(), nullable=True),
    sa.Column('date_imposed', sa.Date(), nullable=True),
    sa.Column('completion_date', sa.Date(), nullable=True),
    sa.Column('projected_completion_date', sa.Date(), nullable=True),
    sa.Column('is_life', sa.Boolean(), nullable=True),
    sa.Column('is_probation', sa.Boolean(), nullable=True),
    sa.Column('is_suspended', sa.Boolean(), nullable=True),
    sa.Column('fine_dollars', sa.Integer(), nullable=True),
    sa.Column('parole_possible', sa.Boolean(), nullable=True),
    sa.Column('post_release_supervision_length_days', sa.Integer(), nullable=True),
    sa.Column('sentence_id', sa.Integer(), nullable=False),
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['booking_id'], ['booking.booking_id'], initially='DEFERRED', deferrable=True),
    sa.PrimaryKeyConstraint('sentence_id')
    )
    op.create_index(op.f('ix_sentence_external_id'), 'sentence', ['external_id'], unique=False)
    op.create_table('arrest_history',
    sa.Column('external_id', sa.String(length=255), nullable=True),
    sa.Column('arrest_date', sa.Date(), nullable=True),
    sa.Column('location', sa.String(length=255), nullable=True),
    sa.Column('agency', sa.String(length=255), nullable=True),
    sa.Column('officer_name', sa.String(length=255), nullable=True),
    sa.Column('officer_id', sa.String(length=255), nullable=True),
    sa.Column('arrest_history_id', sa.Integer(), nullable=False),
    sa.Column('arrest_id', sa.Integer(), nullable=False),
    sa.Column('valid_from', sa.DateTime(), nullable=False),
    sa.Column('valid_to', sa.DateTime(), nullable=True),
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['arrest_id'], ['arrest.arrest_id'], ),
    sa.ForeignKeyConstraint(['booking_id'], ['booking.booking_id'], ),
    sa.PrimaryKeyConstraint('arrest_history_id')
    )
    op.create_index(op.f('ix_arrest_history_arrest_id'), 'arrest_history', ['arrest_id'], unique=False)
    op.create_index(op.f('ix_arrest_history_external_id'), 'arrest_history', ['external_id'], unique=False)
    op.create_table('bond_history',
    sa.Column('external_id', sa.String(length=255), nullable=True),
    sa.Column('amount_dollars', sa.Integer(), nullable=True),
    sa.Column('bond_type', sa.Enum('EXTERNAL_UNKNOWN', 'CASH', 'NO_BOND', 'PARTIAL_CASH', 'SECURED', 'REMOVED_WITHOUT_INFO', 'UNSECURED', name='bond_type'), nullable=True),
    sa.Column('bond_type_raw_text', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Enum('DENIED', 'PRESENT_WITHOUT_INFO', 'INFERRED_SET', 'NOT_REQUIRED', 'PENDING', 'POSTED', 'REVOKED', 'REMOVED_WITHOUT_INFO', 'SET', name='bond_status'), nullable=False),
    sa.Column('status_raw_text', sa.String(length=255), nullable=True),
    sa.Column('bond_agent', sa.String(length=255), nullable=True),
    sa.Column('bond_history_id', sa.Integer(), nullable=False),
    sa.Column('bond_id', sa.Integer(), nullable=False),
    sa.Column('valid_from', sa.DateTime(), nullable=False),
    sa.Column('valid_to', sa.DateTime(), nullable=True),
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['bond_id'], ['bond.bond_id'], ),
    sa.ForeignKeyConstraint(['booking_id'], ['booking.booking_id'], initially='DEFERRED', deferrable=True),
    sa.PrimaryKeyConstraint('bond_history_id')
    )
    op.create_index(op.f('ix_bond_history_bond_id'), 'bond_history', ['bond_id'], unique=False)
    op.create_index(op.f('ix_bond_history_external_id'), 'bond_history', ['external_id'], unique=False)
    op.create_table('charge',
    sa.Column('external_id', sa.String(length=255), nullable=True),
    sa.Column('offense_date', sa.Date(), nullable=True),
    sa.Column('statute', sa.String(length=255), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('attempted', sa.Boolean(), nullable=True),
    sa.Column('degree', sa.Enum('EXTERNAL_UNKNOWN', 'FIRST', 'FOURTH', 'SECOND', 'THIRD', name='degree'), nullable=True),
    sa.Column('degree_raw_text', sa.String(length=255), nullable=True),
    sa.Column('class', sa.Enum('CIVIL', 'EXTERNAL_UNKNOWN', 'FELONY', 'INFRACTION', 'MISDEMEANOR', 'OTHER', 'PAROLE_VIOLATION', 'PROBATION_VIOLATION', name='charge_class'), nullable=True),
    sa.Column('class_raw_text', sa.String(length=255), nullable=True),
    sa.Column('level', sa.String(length=255), nullable=True),
    sa.Column('fee_dollars', sa.Integer(), nullable=True),
    sa.Column('charging_entity', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Enum('ACQUITTED', 'COMPLETED_SENTENCE', 'CONVICTED', 'DROPPED', 'INFERRED_DROPPED', 'EXTERNAL_UNKNOWN', 'PENDING', 'PRETRIAL', 'SENTENCED', 'PRESENT_WITHOUT_INFO', 'REMOVED_WITHOUT_INFO', name='charge_status'), nullable=False),
    sa.Column('status_raw_text', sa.String(length=255), nullable=True),
    sa.Column('court_type', sa.Enum('CIRCUIT', 'CIVIL', 'DISTRICT', 'EXTERNAL_UNKNOWN', 'OTHER', 'SUPERIOR', name='court_type'), nullable=True),
    sa.Column('court_type_raw_text', sa.String(length=255), nullable=True),
    sa.Column('case_number', sa.String(length=255), nullable=True),
    sa.Column('next_court_date', sa.Date(), nullable=True),
    sa.Column('judge_name', sa.String(length=255), nullable=True),
    sa.Column('charge_notes', sa.Text(), nullable=True),
    sa.Column('charge_id', sa.Integer(), nullable=False),
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.Column('bond_id', sa.Integer(), nullable=True),
    sa.Column('sentence_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bond_id'], ['bond.bond_id'], ),
    sa.ForeignKeyConstraint(['booking_id'], ['booking.booking_id'], ),
    sa.ForeignKeyConstraint(['sentence_id'], ['sentence.sentence_id'], ),
    sa.PrimaryKeyConstraint('charge_id')
    )
    op.create_index(op.f('ix_charge_external_id'), 'charge', ['external_id'], unique=False)
    op.create_table('hold_history',
    sa.Column('external_id', sa.String(length=255), nullable=True),
    sa.Column('jurisdiction_name', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Enum('ACTIVE', 'INACTIVE', 'INFERRED_DROPPED', 'PRESENT_WITHOUT_INFO', 'REMOVED_WITHOUT_INFO', name='hold_status'), nullable=False),
    sa.Column('status_raw_text', sa.String(length=255), nullable=True),
    sa.Column('hold_history_id', sa.Integer(), nullable=False),
    sa.Column('hold_id', sa.Integer(), nullable=False),
    sa.Column('valid_from', sa.DateTime(), nullable=False),
    sa.Column('valid_to', sa.DateTime(), nullable=True),
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['booking_id'], ['booking.booking_id'], ),
    sa.ForeignKeyConstraint(['hold_id'], ['hold.hold_id'], ),
    sa.PrimaryKeyConstraint('hold_history_id')
    )
    op.create_index(op.f('ix_hold_history_external_id'), 'hold_history', ['external_id'], unique=False)
    op.create_index(op.f('ix_hold_history_hold_id'), 'hold_history', ['hold_id'], unique=False)
    op.create_table('sentence_history',
    sa.Column('external_id', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Enum('COMMUTED', 'COMPLETED', 'SERVING', 'PRESENT_WITHOUT_INFO', 'REMOVED_WITHOUT_INFO', name='sentence_status'), nullable=False),
    sa.Column('status_raw_text', sa.String(length=255), nullable=True),
    sa.Column('sentencing_region', sa.String(length=255), nullable=True),
    sa.Column('min_length_days', sa.Integer(), nullable=True),
    sa.Column('max_length_days', sa.Integer(), nullable=True),
    sa.Column('date_imposed', sa.Date(), nullable=True),
    sa.Column('completion_date', sa.Date(), nullable=True),
    sa.Column('projected_completion_date', sa.Date(), nullable=True),
    sa.Column('is_life', sa.Boolean(), nullable=True),
    sa.Column('is_probation', sa.Boolean(), nullable=True),
    sa.Column('is_suspended', sa.Boolean(), nullable=True),
    sa.Column('fine_dollars', sa.Integer(), nullable=True),
    sa.Column('parole_possible', sa.Boolean(), nullable=True),
    sa.Column('post_release_supervision_length_days', sa.Integer(), nullable=True),
    sa.Column('sentence_history_id', sa.Integer(), nullable=False),
    sa.Column('sentence_id', sa.Integer(), nullable=False),
    sa.Column('valid_from', sa.DateTime(), nullable=False),
    sa.Column('valid_to', sa.DateTime(), nullable=True),
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['booking_id'], ['booking.booking_id'], initially='DEFERRED', deferrable=True),
    sa.ForeignKeyConstraint(['sentence_id'], ['sentence.sentence_id'], ),
    sa.PrimaryKeyConstraint('sentence_history_id')
    )
    op.create_index(op.f('ix_sentence_history_external_id'), 'sentence_history', ['external_id'], unique=False)
    op.create_index(op.f('ix_sentence_history_sentence_id'), 'sentence_history', ['sentence_id'], unique=False)
    op.create_table('sentence_relationship',
    sa.Column('type', sa.Enum('CONCURRENT', 'CONSECUTIVE', name='sentence_relationship_type'), nullable=False),
    sa.Column('sentence_relation_type_raw_text', sa.String(length=255), nullable=True),
    sa.Column('sentence_relationship_id', sa.Integer(), nullable=False),
    sa.Column('sentence_a_id', sa.Integer(), nullable=False),
    sa.Column('sentence_b_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['sentence_a_id'], ['sentence.sentence_id'], ),
    sa.ForeignKeyConstraint(['sentence_b_id'], ['sentence.sentence_id'], ),
    sa.PrimaryKeyConstraint('sentence_relationship_id')
    )
    op.create_table('charge_history',
    sa.Column('external_id', sa.String(length=255), nullable=True),
    sa.Column('offense_date', sa.Date(), nullable=True),
    sa.Column('statute', sa.String(length=255), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('attempted', sa.Boolean(), nullable=True),
    sa.Column('degree', sa.Enum('EXTERNAL_UNKNOWN', 'FIRST', 'FOURTH', 'SECOND', 'THIRD', name='degree'), nullable=True),
    sa.Column('degree_raw_text', sa.String(length=255), nullable=True),
    sa.Column('class', sa.Enum('CIVIL', 'EXTERNAL_UNKNOWN', 'FELONY', 'INFRACTION', 'MISDEMEANOR', 'OTHER', 'PAROLE_VIOLATION', 'PROBATION_VIOLATION', name='charge_class'), nullable=True),
    sa.Column('class_raw_text', sa.String(length=255), nullable=True),
    sa.Column('level', sa.String(length=255), nullable=True),
    sa.Column('fee_dollars', sa.Integer(), nullable=True),
    sa.Column('charging_entity', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Enum('ACQUITTED', 'COMPLETED_SENTENCE', 'CONVICTED', 'DROPPED', 'INFERRED_DROPPED', 'EXTERNAL_UNKNOWN', 'PENDING', 'PRETRIAL', 'SENTENCED', 'PRESENT_WITHOUT_INFO', 'REMOVED_WITHOUT_INFO', name='charge_status'), nullable=False),
    sa.Column('status_raw_text', sa.String(length=255), nullable=True),
    sa.Column('court_type', sa.Enum('CIRCUIT', 'CIVIL', 'DISTRICT', 'EXTERNAL_UNKNOWN', 'OTHER', 'SUPERIOR', name='court_type'), nullable=True),
    sa.Column('court_type_raw_text', sa.String(length=255), nullable=True),
    sa.Column('case_number', sa.String(length=255), nullable=True),
    sa.Column('next_court_date', sa.Date(), nullable=True),
    sa.Column('judge_name', sa.String(length=255), nullable=True),
    sa.Column('charge_notes', sa.Text(), nullable=True),
    sa.Column('charge_history_id', sa.Integer(), nullable=False),
    sa.Column('charge_id', sa.Integer(), nullable=False),
    sa.Column('valid_from', sa.DateTime(), nullable=False),
    sa.Column('valid_to', sa.DateTime(), nullable=True),
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.Column('bond_id', sa.Integer(), nullable=True),
    sa.Column('sentence_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['bond_id'], ['bond.bond_id'], ),
    sa.ForeignKeyConstraint(['booking_id'], ['booking.booking_id'], ),
    sa.ForeignKeyConstraint(['charge_id'], ['charge.charge_id'], ),
    sa.ForeignKeyConstraint(['sentence_id'], ['sentence.sentence_id'], ),
    sa.PrimaryKeyConstraint('charge_history_id')
    )
    op.create_index(op.f('ix_charge_history_charge_id'), 'charge_history', ['charge_id'], unique=False)
    op.create_index(op.f('ix_charge_history_external_id'), 'charge_history', ['external_id'], unique=False)
    op.create_table('sentence_relationship_history',
    sa.Column('type', sa.Enum('CONCURRENT', 'CONSECUTIVE', name='sentence_relationship_type'), nullable=False),
    sa.Column('sentence_relation_type_raw_text', sa.String(length=255), nullable=True),
    sa.Column('sentence_relationship_history_id', sa.Integer(), nullable=False),
    sa.Column('sentence_relationship_id', sa.Integer(), nullable=False),
    sa.Column('valid_from', sa.DateTime(), nullable=False),
    sa.Column('valid_to', sa.DateTime(), nullable=True),
    sa.Column('sentence_a_id', sa.Integer(), nullable=False),
    sa.Column('sentence_b_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['sentence_a_id'], ['sentence.sentence_id'], ),
    sa.ForeignKeyConstraint(['sentence_b_id'], ['sentence.sentence_id'], ),
    sa.ForeignKeyConstraint(['sentence_relationship_id'], ['sentence_relationship.sentence_relationship_id'], ),
    sa.PrimaryKeyConstraint('sentence_relationship_history_id')
    )
    op.create_index(op.f('ix_sentence_relationship_history_sentence_relationship_id'), 'sentence_relationship_history', ['sentence_relationship_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_sentence_relationship_history_sentence_relationship_id'), table_name='sentence_relationship_history')
    op.drop_table('sentence_relationship_history')
    op.drop_index(op.f('ix_charge_history_external_id'), table_name='charge_history')
    op.drop_index(op.f('ix_charge_history_charge_id'), table_name='charge_history')
    op.drop_table('charge_history')
    op.drop_table('sentence_relationship')
    op.drop_index(op.f('ix_sentence_history_sentence_id'), table_name='sentence_history')
    op.drop_index(op.f('ix_sentence_history_external_id'), table_name='sentence_history')
    op.drop_table('sentence_history')
    op.drop_index(op.f('ix_hold_history_hold_id'), table_name='hold_history')
    op.drop_index(op.f('ix_hold_history_external_id'), table_name='hold_history')
    op.drop_table('hold_history')
    op.drop_index(op.f('ix_charge_external_id'), table_name='charge')
    op.drop_table('charge')
    op.drop_index(op.f('ix_bond_history_external_id'), table_name='bond_history')
    op.drop_index(op.f('ix_bond_history_bond_id'), table_name='bond_history')
    op.drop_table('bond_history')
    op.drop_index(op.f('ix_arrest_history_external_id'), table_name='arrest_history')
    op.drop_index(op.f('ix_arrest_history_arrest_id'), table_name='arrest_history')
    op.drop_table('arrest_history')
    op.drop_index(op.f('ix_sentence_external_id'), table_name='sentence')
    op.drop_table('sentence')
    op.drop_index(op.f('ix_hold_external_id'), table_name='hold')
    op.drop_table('hold')
    op.drop_index(op.f('ix_booking_history_external_id'), table_name='booking_history')
    op.drop_index(op.f('ix_booking_history_booking_id'), table_name='booking_history')
    op.drop_table('booking_history')
    op.drop_index(op.f('ix_bond_external_id'), table_name='bond')
    op.drop_table('bond')
    op.drop_index(op.f('ix_arrest_external_id'), table_name='arrest')
    op.drop_table('arrest')
    op.drop_index(op.f('ix_person_history_region'), table_name='person_history')
    op.drop_index(op.f('ix_person_history_person_id'), table_name='person_history')
    op.drop_index(op.f('ix_person_history_external_id'), table_name='person_history')
    op.drop_table('person_history')
    op.drop_index(op.f('ix_booking_external_id'), table_name='booking')
    op.drop_table('booking')
    op.drop_index(op.f('ix_person_region'), table_name='person')
    op.drop_index(op.f('ix_person_full_name'), table_name='person')
    op.drop_index(op.f('ix_person_external_id'), table_name='person')
    op.drop_index(op.f('ix_person_birthdate'), table_name='person')
    op.drop_table('person')
    # ### end Alembic commands ###