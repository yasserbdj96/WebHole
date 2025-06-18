package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
)

func main() {
	path := "."
	if len(os.Args) > 1 {
		path = os.Args[1]
	}

	output := ls(path)
	fmt.Println(output)
}

func ls(path string) string {
	// Normalize the path
	absPath, err := filepath.Abs(path)
	if err != nil {
		errMsg, _ := json.Marshal([]string{fmt.Sprintf("❌ Error: %v", err)})
		return string(errMsg)
	}

	// Ensure drive like "D:" becomes "D:\"
	if len(absPath) == 2 && absPath[1] == ':' {
		absPath += `\`
	}

	// Check existence
	if _, err := os.Stat(absPath); os.IsNotExist(err) {
		errMsg, _ := json.Marshal([]string{fmt.Sprintf("❌ Error: '%s' not found.", absPath)})
		return string(errMsg)
	}

	// Read directory
	entries, err := os.ReadDir(absPath)
	if err != nil {
		errMsg, _ := json.Marshal([]string{fmt.Sprintf("❌ Error: %v", err)})
		return string(errMsg)
	}

	var result []string
	for _, entry := range entries {
		name := entry.Name()
		if entry.IsDir() {
			result = append(result, "📁 "+name)
		} else {
			result = append(result, "📄 "+name)
		}
	}

	jsonResult, err := json.Marshal(result)
	if err != nil {
		errMsg, _ := json.Marshal([]string{fmt.Sprintf("❌ Error: %v", err)})
		return string(errMsg)
	}

	return string(jsonResult)
}
