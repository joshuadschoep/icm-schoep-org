import { Form as FormProvider } from "@/components/ui/form";
import { Separator } from "../ui/separator";
import { Button } from "../ui/button";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { PlayersForm } from "./comps/players";
import { DefaultValues, FormSchema } from "./schema";
import { PayoutsForm } from "./comps/payouts";
import { useCallback, useState } from "react";
import axios from "axios";
import { Results } from "../results/results";
import { Selection } from "./comps/selection";
import { Loader2Icon } from "lucide-react";

export const Form = () => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState("");

  const form = useForm({
    resolver: zodResolver(FormSchema),
    defaultValues: DefaultValues,
  });

  const onFinalSubmit = useCallback(
    async (data: any) => {
      setLoading(true);
      setApiError("");
      setResults([]);
      let result: any;
      try {
        if (form.watch("method") === "tysen") {
          result = await axios.post(
            `${import.meta.env.PUBLIC_API_URI}/solutions/tysen`,
            data
          );
        } else {
          result = await axios.post(
            `${import.meta.env.PUBLIC_API_URI}/solutions/malmuth-harville`,
            data
          );
        }

        setLoading(false);

        if (result.status === 200) {
          setResults(result.data.results);
        } else if (result.status >= 400 && result.status <= 499) {
          setApiError("An error has occured. Please try again.");
        } else if (result.status >= 500 && result.status <= 599) {
          setApiError(
            "An error has occured. We apologize for the inconvenience."
          );
        }
      } catch (e) {
        setLoading(false);
        setApiError("An error has occured. Please try again.");
      }
    },
    [setApiError, form.watch("method")]
  );

  return (
    <div>
      <FormProvider {...form}>
        <form onSubmit={form.handleSubmit(onFinalSubmit)}>
          <section className="px-6 pb-0 grid gap-3 md:grid-cols-[1fr_auto_2fr]">
            <PayoutsForm />
            <Separator orientation="vertical" />
            <PlayersForm />
          </section>
          <Separator />
          <section className="col-span-3 flex flex-col gap-6 md:flex-row md:gap-3 items-center md:justify-between p-5">
            <Selection />
            <Button
              type="submit"
              disabled={loading}
              className="cursor-pointer w-full md:w-60 block bg-emerald-600 hover:bg-emerald-700 flex items-center"
            >
              {loading && <Loader2Icon className="animate-spin" />}
              Calculate
            </Button>
          </section>
        </form>
        <Separator />
      </FormProvider>
      <div
        className={
          (results && results.length > 0) || apiError
            ? "scale-y-100 origin-top duration-500"
            : "scale-y-0 origin-top"
        }
      >
        {apiError && <p className="p-5 text-center text-red-500">{apiError}</p>}
        {results && results.length > 0 && <Results results={results} />}
      </div>
    </div>
  );
};
