import React, { useMemo } from 'react';
import DataTable from './DataTable';

const TableWrapper = ({ title, data }) => {
  const columns = useMemo(
    () => Object.keys(data).map(key => ({ Header: key, accessor: key })),
    [data]
  );

  const tableData = useMemo(
    () => [data],
    [data]
  );

  return (
    <div>
      <h2>{title}</h2>
      <DataTable columns={columns} data={tableData} />
    </div>
  );
};

export default TableWrapper;