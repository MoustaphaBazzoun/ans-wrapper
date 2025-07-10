"""
Modulo de Beneficiários
"""

from datetime import datetime
from typing import List

import pandas as pd
import requests

from ans_wrapper.beneficiarios_utils import parse_url_links

BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/"
# Concept:
# region, time_interval,


class Beneficiarios:
	ENDPOINT = "informacoes_consolidadas_de_beneficiarios-024/"
	BENEFICIARIOS_URL = BASE_URL + ENDPOINT

	def __init__(self):
		self.available_months = self._fetch_available_months()

	def _fetch_available_months(self) -> List[str]:
		"""
		Fetches the list of available months from the beneficiários folder.

		Returns:
			List[str]: A sorted list of strings in the format 'YYYYMM',
					   representing each available monthly folder on the server.
		"""
		# Fetching the page data
		list_of_links = parse_url_links(self.BENEFICIARIOS_URL)

		# Parsing and cleaning links
		list_of_dates = []
		for link in list_of_links:
			href = link["href"]
			# if it's a folder and name starts with a 6-digit date
			if href.endswith("/") and href[:6].isdigit():
				list_of_dates.append(href.strip("/"))

		return list_of_dates

	@property
	def date_range(self):
		"""Range of available data"""
		if not self.available_months:
			return "No data available"

		start = (datetime
				.strptime(self.available_months[0], "%Y%m")
				.strftime("%b %Y"))
		
		end = (datetime
			  .strptime(self.available_months[-1], "%Y%m")
			  .strftime("%b %Y"))

		return f"data available from {start} to {end}"
	
	@property
	def info(self) -> str:
		return (
			f"Beneficiários data available:\n"
			f"📅 {self.date_range}\n"
			f"📦 {len(self.available_months)} months available\n"
			f"🔗 Source: {self.BENEFICIARIOS_URL}"
		)

	def hello():
		pass
	

	def build_dataset(
		start,
		end,
		range
		) -> pd.DataFrame:
		"""Create a dataset using customized configs."""
		pass
