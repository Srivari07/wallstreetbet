import { useMemo, useEffect, useState } from "react";

export default function useTickerToTable() {
  const [apiData, setApiData] = useState([]);

  useEffect(() => {
    fetch("/data")
      .then((res) => res.json())
      .then((data) => setApiData(data.data));
  }, []);

  const data = useMemo(
    () =>
      apiData.map((tickerData) => {
        return { ...tickerData };
      }),
    [apiData]
  );

  const columns = useMemo(
    () => [
      {
        Header: "Ticker",

        accessor: "Ticker",
      },

      {
        Header: "Mentions",

        accessor: "Mentions",
      },
      {
        Header: "Previous Close",

        accessor: "PreviousClose",
      },
      {
        Header: "Open",

        accessor: "Open",
      },
      {
        Header: "Low",

        accessor: "Low",
      },
      {
        Header: "High",

        accessor: "High",
      },
      {
        Header: "Price",

        accessor: "Price",
      },
      {
        Header: "Change Percent",

        accessor: "ChangePercent",
      },
    ],
    []
  );

  return { data, columns };
}
