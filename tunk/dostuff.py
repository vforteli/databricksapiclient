# Databricks notebook source
from argparser import parse_params, return_meaning_of_life

# get parameters for job, usually from datafactory
# this should probably always be run first...
# dbutils.widgets.text("some_param", "default_value")
# some_param = dbutils.widgets.get("some_param")
# print(f"User input: {some_param}")

meaning_of_life = return_meaning_of_life()
# parsed_params = parse_params(dbutils.notebook.entry_point.getCurrentBindings())

print(meaning_of_life)


# COMMAND ----------


display("Starting the job... :D")

dbutils.notebook.exit(f"Hello {some_param}")
