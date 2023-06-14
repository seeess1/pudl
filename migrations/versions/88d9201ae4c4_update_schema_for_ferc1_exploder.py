"""update schema for ferc1 exploder

Revision ID: 88d9201ae4c4
Revises: 92780dd3d879
Create Date: 2023-06-08 11:04:31.244964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88d9201ae4c4'
down_revision = '92780dd3d879'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('denorm_depreciation_amortization_summary_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dollar_value', sa.Float(), nullable=True, comment='Dollar value of reported income, expense, asset, or liability.'))
        batch_op.drop_column('depreciation_amortization_value')

    with op.batch_alter_table('denorm_electric_operating_expenses_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dollar_value', sa.Float(), nullable=True, comment='Dollar value of reported income, expense, asset, or liability.'))
        batch_op.drop_column('expense')

    with op.batch_alter_table('denorm_electric_operating_revenues_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dollar_value', sa.Float(), nullable=True, comment='Dollar value of reported income, expense, asset, or liability.'))
        batch_op.add_column(sa.Column('ferc_account', sa.Text(), nullable=True, comment="Actual FERC Account number (e.g. '359.1') if available, or a PUDL assigned ID when FERC accounts have been split or combined in reporting."))
        batch_op.add_column(sa.Column('row_type_xbrl', sa.Enum('calculated_value', 'reported_value', 'correction'), nullable=True, comment='Indicates whether the value reported in the row is calculated, or uniquely reported within the table.'))
        batch_op.drop_column('revenue')

    with op.batch_alter_table('denorm_electric_plant_depreciation_functional_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ending_balance', sa.Float(), nullable=True, comment='Account balance at end of year.'))
        batch_op.drop_column('utility_plant_value')

    with op.batch_alter_table('denorm_electricity_sales_by_rate_schedule_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dollar_value', sa.Float(), nullable=True, comment='Dollar value of reported income, expense, asset, or liability.'))
        batch_op.drop_column('sales_revenue')

    with op.batch_alter_table('denorm_income_statement_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dollar_value', sa.Float(), nullable=True, comment='Dollar value of reported income, expense, asset, or liability.'))
        batch_op.drop_column('income')

    with op.batch_alter_table('denorm_plant_in_service_ferc1', schema=None) as batch_op:
        batch_op.alter_column('report_year',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('utility_id_ferc1',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('record_id',
               existing_type=sa.TEXT(),
               nullable=True)

    with op.batch_alter_table('denorm_utility_plant_summary_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ending_balance', sa.Float(), nullable=True, comment='Account balance at end of year.'))
        batch_op.drop_column('utility_plant_value')

    with op.batch_alter_table('depreciation_amortization_summary_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dollar_value', sa.Float(), nullable=True, comment='Dollar value of reported income, expense, asset, or liability.'))
        batch_op.drop_column('depreciation_amortization_value')

    with op.batch_alter_table('electric_operating_expenses_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dollar_value', sa.Float(), nullable=True, comment='Dollar value of reported income, expense, asset, or liability.'))
        batch_op.drop_column('expense')

    with op.batch_alter_table('electric_operating_revenues_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dollar_value', sa.Float(), nullable=True, comment='Dollar value of reported income, expense, asset, or liability.'))
        batch_op.add_column(sa.Column('ferc_account', sa.Text(), nullable=True, comment="Actual FERC Account number (e.g. '359.1') if available, or a PUDL assigned ID when FERC accounts have been split or combined in reporting."))
        batch_op.add_column(sa.Column('row_type_xbrl', sa.Enum('calculated_value', 'reported_value', 'correction'), nullable=True, comment='Indicates whether the value reported in the row is calculated, or uniquely reported within the table.'))
        batch_op.drop_column('revenue')

    with op.batch_alter_table('electric_plant_depreciation_functional_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ending_balance', sa.Float(), nullable=True, comment='Account balance at end of year.'))
        batch_op.drop_column('utility_plant_value')

    with op.batch_alter_table('electricity_sales_by_rate_schedule_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dollar_value', sa.Float(), nullable=True, comment='Dollar value of reported income, expense, asset, or liability.'))
        batch_op.drop_column('sales_revenue')

    with op.batch_alter_table('income_statement_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dollar_value', sa.Float(), nullable=True, comment='Dollar value of reported income, expense, asset, or liability.'))
        batch_op.drop_column('income')

    with op.batch_alter_table('utility_plant_summary_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ending_balance', sa.Float(), nullable=True, comment='Account balance at end of year.'))
        batch_op.drop_column('utility_plant_value')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('utility_plant_summary_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('utility_plant_value', sa.FLOAT(), nullable=True))
        batch_op.drop_column('ending_balance')

    with op.batch_alter_table('income_statement_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('income', sa.FLOAT(), nullable=True))
        batch_op.drop_column('dollar_value')

    with op.batch_alter_table('electricity_sales_by_rate_schedule_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sales_revenue', sa.FLOAT(), nullable=True))
        batch_op.drop_column('dollar_value')

    with op.batch_alter_table('electric_plant_depreciation_functional_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('utility_plant_value', sa.FLOAT(), nullable=True))
        batch_op.drop_column('ending_balance')

    with op.batch_alter_table('electric_operating_revenues_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('revenue', sa.FLOAT(), nullable=True))
        batch_op.drop_column('row_type_xbrl')
        batch_op.drop_column('ferc_account')
        batch_op.drop_column('dollar_value')

    with op.batch_alter_table('electric_operating_expenses_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('expense', sa.FLOAT(), nullable=True))
        batch_op.drop_column('dollar_value')

    with op.batch_alter_table('depreciation_amortization_summary_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('depreciation_amortization_value', sa.FLOAT(), nullable=True))
        batch_op.drop_column('dollar_value')

    with op.batch_alter_table('denorm_utility_plant_summary_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('utility_plant_value', sa.FLOAT(), nullable=True))
        batch_op.drop_column('ending_balance')

    with op.batch_alter_table('denorm_plant_in_service_ferc1', schema=None) as batch_op:
        batch_op.alter_column('record_id',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('utility_id_ferc1',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('report_year',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('denorm_income_statement_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('income', sa.FLOAT(), nullable=True))
        batch_op.drop_column('dollar_value')

    with op.batch_alter_table('denorm_electricity_sales_by_rate_schedule_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sales_revenue', sa.FLOAT(), nullable=True))
        batch_op.drop_column('dollar_value')

    with op.batch_alter_table('denorm_electric_plant_depreciation_functional_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('utility_plant_value', sa.FLOAT(), nullable=True))
        batch_op.drop_column('ending_balance')

    with op.batch_alter_table('denorm_electric_operating_revenues_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('revenue', sa.FLOAT(), nullable=True))
        batch_op.drop_column('row_type_xbrl')
        batch_op.drop_column('ferc_account')
        batch_op.drop_column('dollar_value')

    with op.batch_alter_table('denorm_electric_operating_expenses_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('expense', sa.FLOAT(), nullable=True))
        batch_op.drop_column('dollar_value')

    with op.batch_alter_table('denorm_depreciation_amortization_summary_ferc1', schema=None) as batch_op:
        batch_op.add_column(sa.Column('depreciation_amortization_value', sa.FLOAT(), nullable=True))
        batch_op.drop_column('dollar_value')

    # ### end Alembic commands ###