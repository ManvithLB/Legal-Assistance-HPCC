import React, { useState } from "react";
import { Table, Thead, Tbody, Tr, Th, Td, Button } from "@chakra-ui/react";

interface ResponseData {
  roxie_index_search_2Response: {
    Results: {
      result_1: {
        Row: {
          text_id: string;
          text: string;
        }[];
      };
    };
  };
}

interface Props {
  data: ResponseData;
}

const DataTable: React.FC<Props> = ({ data }) => {
  const extractedResults =
    data?.roxie_index_search_2Response?.Results?.result_1?.Row || [];

  const [expandedRows, setExpandedRows] = useState<number[]>([]);

  const toggleRowExpansion = (index: number) => {
    if (expandedRows.includes(index)) {
      setExpandedRows(expandedRows.filter((rowIndex) => rowIndex !== index));
    } else {
      setExpandedRows([...expandedRows, index]);
    }
  };

  const isRowExpanded = (index: number) => {
    return expandedRows.includes(index);
  };

  const renderText = (text: string, index: number) => {
    const maxLength = 300; // Adjust the maximum length as per your requirement

    if (isRowExpanded(index)) {
      return text;
    } else {
      return text.length > maxLength ? text.slice(0, maxLength) + "..." : text;
    }
  };

  return (
    <Table variant="simple">
      <Thead>
        <Tr>
          <Th>Text Id</Th>
          <Th>Text</Th>
        </Tr>
      </Thead>
      <Tbody>
        {extractedResults.map((result, index) => (
          <Tr key={index}>
            <Td>{result.text_id}</Td>
            <Td>
              {renderText(result.text, index)}
              {result.text.length > 100 && (
                <Button
                  onClick={() => toggleRowExpansion(index)}
                  style={{ marginLeft: "8px" }}
                >
                  {isRowExpanded(index) ? "View Less" : "View More"}
                </Button>
              )}
            </Td>
          </Tr>
        ))}
      </Tbody>
    </Table>
  );
};

export default DataTable;
