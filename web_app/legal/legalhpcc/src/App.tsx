import React, { useState } from "react";
import {
  Textarea,
  Spinner,
  Alert,
  AlertIcon,
  Tag,
  TagLabel,
  TagCloseButton,
  Button,
  VStack,
  HStack,
  Badge,
  CloseButton,
} from "@chakra-ui/react";
import axios from "axios";
import { WithContext as ReactTags } from "react-tag-input";
import sendRoxieRequest from "./components/sendRoxieRequest";
import DataTable from "./components/DataTable";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [keywords, setKeywords] = useState([]);
  const [results, setResults] = useState(null);

  const handleChange = (e) => {
    setText(e.target.value);
  };

  // const handleDelete = (i) => {
  //   const newKeywords = keywords.slice(0);
  //   newKeywords.splice(i, 1);
  //   setKeywords(newKeywords);
  // };

  // const handleAddition = (tag) => {
  //   setKeywords([...keywords, tag.text]);
  // };

  const handleSubmit = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await axios.post("http://localhost:5000/process_text", {
        text,
      });
      const data = response.data;
      setKeywords(data.keywords.split(", "));
    } catch (error) {
      setError("An error occurred while processing the text.");
    } finally {
      setLoading(false);
    }
  };

  const handleSendRoxieRequest = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await axios.post("http://localhost:5000/sendroxie", {
        keywords: keywords.join(", "),
      });
      setResults(response.data);
    } catch (error) {
      setError("An error occurred while sending request to Roxie.");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = (i) => {
    setKeywords((prevKeywords) =>
      prevKeywords.filter((keyword, index) => index !== i)
    );
  };

  const handleAddition = (tag) => {
    const newKeywords = [...keywords, tag.text];
    setKeywords(newKeywords);
  };
  const handleDrag = (tag, currPos, newPos) => {
    const newKeywords = [...keywords];
    const movedTag = newKeywords.splice(currPos, 1)[0];
    newKeywords.splice(newPos, 0, movedTag);
    setKeywords(newKeywords);
  };

  return (
    <VStack p={4} spacing={4} align="stretch">
      <Textarea
        value={text}
        onChange={handleChange}
        placeholder="Enter text..."
      />
      <Button onClick={handleSubmit} isLoading={loading}>
        Submit
      </Button>
      {error && <p>{error}</p>}

      <ReactTags
        tags={keywords.map((keyword, index) => ({
          id: index.toString(),
          text: keyword,
        }))}
        handleDelete={handleDelete}
        handleAddition={handleAddition}
        handleDrag={handleDrag}
        allowDragDrop={true}
        autofocus={false}
        placeholder="Add new keyword"
        classNames={{
          tags: "custom-tags",
          tagInput: "custom-tag-input",
          tagInputField: "custom-tag-input-field",
          selected: "custom-selected",
          tag: "custom-tag",
          remove: "custom-remove",
          suggestions: "custom-suggestions",
          activeSuggestion: "custom-active-suggestion",
          editTagInput: "custom-edit-tag-input",
          editTagInputField: "custom-edit-tag-input-field",
          clearAll: "custom-clear-all",
        }}
      />
      <Button onClick={handleSendRoxieRequest} isLoading={loading}>
        Send Request to Roxie
      </Button>
      {results && <DataTable data={results} />}
    </VStack>
  );
}

export default App;
