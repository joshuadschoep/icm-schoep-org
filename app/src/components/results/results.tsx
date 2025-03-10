import { ChartPie, ChevronDown, DollarSign } from "lucide-react";
import {
  Table,
  TableBody,
  TableCell,
  TableFooter,
  TableHead,
  TableHeader,
  TableRow,
} from "../ui/table";
import { Separator } from "../ui/separator";
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "../ui/chart";
import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from "recharts";

type Results = Array<{
  name?: string;
  stack: number;
  payout: number;
}>;

interface Props {
  results: Results;
}

const chartConfig = {
  payout: {
    label: "Payout",
    icon: DollarSign,
    color: "#2563eb",
  },
  ratio: {
    label: "Chip Effect",
    icon: ChartPie,
    color: "#e3b625",
  },
} satisfies ChartConfig;

export const Results = ({ results }: Props) => {
  return (
    <section className="p-5 gap-12 grid md:grid-cols-2">
      <h2 className="text-lg text-center md:col-span-2 gap-6">Results</h2>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Name</TableHead>
            <TableHead>
              <span className="flex items-center">
                Stack Size <ChevronDown />
              </span>
            </TableHead>
            <TableHead>Payout</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {results.map((result) => (
            <TableRow key={`${result.name}-${result.stack}`}>
              <TableCell>{result.name}</TableCell>
              <TableCell>{result.stack}</TableCell>
              <TableCell>{result.payout}</TableCell>
            </TableRow>
          ))}
        </TableBody>
        <TableFooter>
          <TableRow>
            <TableCell colSpan={2}>Total</TableCell>
            <TableCell>
              {results.reduce(
                (running, current) => running + current.payout,
                0
              )}
            </TableCell>
          </TableRow>
        </TableFooter>
      </Table>
      <div>
        <h3 className="mb-3">Payouts per player</h3>
        <ChartContainer config={chartConfig}>
          <BarChart accessibilityLayer data={results}>
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey={(val) => val.name || val.stack}
              axisLine={false}
              tickLine={false}
              tickMargin={10}
            />
            <YAxis dataKey="payout" />
            <ChartTooltip content={<ChartTooltipContent hideLabel />} />
            <Bar dataKey="payout" fill="var(--color-payout)" radius={4} />
          </BarChart>
        </ChartContainer>
      </div>
      <div>
        <h3 className="mb-3">Chip Effectiveness (payout / stack value)</h3>
        <ChartContainer config={chartConfig}>
          <BarChart
            accessibilityLayer
            data={results.map((result) => ({
              ...result,
              ratio: result.payout / result.stack,
            }))}
          >
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey={(val) => val.name || val.stack}
              axisLine={false}
              tickLine={false}
              tickMargin={10}
            />
            <YAxis dataKey="ratio" />
            <Bar dataKey="ratio" fill="var(--color-ratio)" radius={4} />
          </BarChart>
        </ChartContainer>
      </div>
    </section>
  );
};
