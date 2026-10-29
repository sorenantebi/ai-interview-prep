import { loader, type BeforeMount, type EditorProps } from "@monaco-editor/react";

// Load the editor from this app (src/app/monaco), not a CDN, so it works offline.
loader.config({ paths: { vs: "/monaco/vs" } });

// No autocomplete, hints or auto-closing in either mode: you type every character, like in a real interview.
export const NO_ASSIST: EditorProps["options"] = {
  automaticLayout: true, // follow the panel when you drag the dividers
  minimap: { enabled: false }, fontSize: 14, fontFamily: "var(--font-jetbrains), monospace", scrollBeyondLastLine: false,
  quickSuggestions: false, suggestOnTriggerCharacters: false, wordBasedSuggestions: "off", parameterHints: { enabled: false },
  acceptSuggestionOnEnter: "off", tabCompletion: "off", snippetSuggestions: "none", inlineSuggest: { enabled: false },
  hover: { enabled: "off" }, autoClosingBrackets: "never", autoClosingQuotes: "never", autoSurround: "never", formatOnType: false,
  occurrencesHighlight: "off", selectionHighlight: false, codeLens: false,
};
// "Doc" = Google-interview style blank white sheet: no highlighting, line numbers, guides or auto-indent.
export const DOC: EditorProps["options"] = {
  ...NO_ASSIST, lineNumbers: "off", glyphMargin: false, folding: false, lineDecorationsWidth: 16, renderLineHighlight: "none",
  guides: { indentation: false, bracketPairs: false }, matchBrackets: "never", autoIndent: "none", renderWhitespace: "none",
  padding: { top: 16 }, wordWrap: "on",
};

// Doc mode's languages: no highlighting, but Cmd/Ctrl+/ (line comment) and Shift+Alt+A (block comment) still know the comment syntax.
export const docLanguage = (lang: "python" | "cpp") => `doc-${lang}`;
export const registerDocLanguages: BeforeMount = (monaco) => {
  if (monaco.languages.getLanguages().some((l: { id: string }) => l.id === "doc-python")) return;
  monaco.languages.register({ id: "doc-python" });
  monaco.languages.setLanguageConfiguration("doc-python", { comments: { lineComment: "#", blockComment: ['"""', '"""'] } });
  monaco.languages.register({ id: "doc-cpp" });
  monaco.languages.setLanguageConfiguration("doc-cpp", { comments: { lineComment: "//", blockComment: ["/*", "*/"] } });
};
