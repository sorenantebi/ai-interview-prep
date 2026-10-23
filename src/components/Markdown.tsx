import ReactMarkdown, { defaultUrlTransform } from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import rehypeRaw from "rehype-raw";
import rehypeSanitize, { defaultSchema } from "rehype-sanitize";
import { resolveRepoUrl } from "@/lib/repo-links";

// GitHub-style allow-list, plus the class names syntax highlighting needs.
const schema = { ...defaultSchema, attributes: { ...defaultSchema.attributes, code: [...(defaultSchema.attributes?.code ?? []), ["className", /^language-/]] } };

/**
 * Renders markdown, dropping the YAML frontmatter.
 * `repo` (for files inside a cloned repo): raw HTML is rendered after sanitising, and relative links/images resolve
 * inside that repo, so a README behaves like it does on GitHub.
 */
export default function Markdown({ children, repo }: { children: string; repo?: { name: string; dir: string } }) {
  const body = children.replace(/^---\n[\s\S]*?\n---\n/, "");
  return (
    <div className="md">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={repo ? [rehypeRaw, [rehypeSanitize, schema], rehypeHighlight] : [rehypeHighlight]}
        urlTransform={repo ? (url, key) => defaultUrlTransform(resolveRepoUrl(url, key, repo)) : undefined}
      >
        {body}
      </ReactMarkdown>
    </div>
  );
}
