# Rapport TP Agents IA

Binômes : REYNAUD Anthéo & LEDOUIT Mathis & RIVAUX Nathan

## Exercices

### Exercice 1.1

```json
{
    'choices': 
        [
            {
                'finish_reason': 'tool_calls', 
                'index': 0, 
                'message': 
                    {
                        'role': 'assistant', 
                        'content': '', 
                        'reasoning_content': 
                            '1.  **Identify the user\'s request:** The user is asking for the result of "15 times 8".\n2.  **Analyze the available tools:** The provided toolset includes a `Calculator` with operations: add, subtract, multiply, divide.\n3.  **Determine the appropriate tool:** The request is a multiplication problem, which directly maps to the `Calculator` tool\'s `multiply` operation.\n4.  **Identify the arguments for the tool:** The `Calculator` requires `operation` (which will be "multiply" or equivalent), `a` (15), and `b` (8).\n5.  **Construct the tool call:**\n    *   Operation: "multiply"\n    *   a: 15\n    *   b: 8\n6.  **Format the output:** Generate the tool call in the required format.', 
                        'tool_calls': 
                            [
                                {
                                    'type': 'function', 
                                    'function': 
                                        {
                                            'name': 'Calculator', 
                                            'arguments': 
                                                '{
                                                    "a":15,
                                                    "b":8,
                                                    "operation":"multiply"
                                                    }'
                                        }, 
                                    'id': 'RliXBfyj4FLANFurBMwQrvCpOd9uLsiH'
                                }
                            ]
                    }
            }
        ], 'created': 1792584639, 'model': '/models/gemma-4-E2B-it-Q4_0.gguf', 'system_fingerprint': 'b11783-339f3242c', 'object': 'chat.completion', 'usage': {'completion_tokens': 213, 'prompt_tokens': 99, 'total_tokens': 312, 'prompt_tokens_details': {'cached_tokens': 94}}, 'id': 'chatcmpl-HOSbysgMYJsnXcNFSBMTwoeiNMVkzNxZ', 'timings': {'cache_n': 94, 'prompt_n': 5, 'prompt_ms': 195.38, 'prompt_per_token_ms': 39.076, 'prompt_per_second': 25.591155696591258, 'predicted_n': 213, 'predicted_ms': 16855.612, 'predicted_per_token_ms': 79.5076037735849, 'predicted_per_second': 12.577413386117335, 'draft_n': 64, 'draft_n_accepted': 6}}
```

L'analyse de reasoning_content semble correcte : l'agent comprend la question en identifiant l'operation mathematique et les opérandes. Puis il étudie les outils disponibles. Il choisit l'outil adapté (Calcultor). Puis il identifie les arguments nécessaires à Calculator. Enfin, il genere la sortie au bon format. 

Il contient les appels aux outils que veux faire le LLM, au format demandé. Ici, un appel à Calculator avec les argument a=15, b=8 et operation=multiply.

Au début de son raisonement, le LLM vérifie si un outil lui est utile, et il l'utilise.

Si l'on ne donne pas l'outil Calculator, il nous donne le raisonnement pour calculer $15\times8$ ($15\times8 = 10\times8 + 5\times8$) et nous retourne au final le calcul. Cela est possible car c'est une opération simple, donc le modele a pu y être entrainé. Mais si on avait besoin d'une opération plus complexe (ex: obtenir la météo en un lieu) et que l'on ne lui fournissait pas l'outil pour, il ne pourrait pas répondre, ou répondrait completement à coté de la plaque.

### Exercice 1.2

On rajoute la réponse du LLM à la liste de message, pour que l'agent ait le contexte du resultat du tool qu'on lui passe.

tool_call_id rappelle au LLM de quel outil il fournit le résultat

Si l'on oublie de mettre le resultat de l'outil, le dernier message est celui de l'assistant, il ne va donc pas se répondre à lui même


Bonus: nous avons remplacé le resultat d'execute_tool par 5. Le LLM s'est alors rendu compte de l'erreur du résultat ("The tool output seems wrong"), et a correctement répondu "15 times 8 is 120." 

### Exercice 1.3

make_tool convertit chaque dataclass au format OpenAI, en précisant automatiquement les paramètres.

Si l'on ajoute un argument, cela peut embrouiller le LLM, car si l'on ne décrit pas les arguments dans la description, le LLM doit deviner leur fonctionnement seulement avec le nom.

Si on rajoute un champ Literal["french", "english"] et une phrase en allemand par exemple, le LLM va comprendre qu'il n'a pas l'option d'indiquer sur le champ que le texte est en allemand. 
Cependant à la fin de son raisonnement, il préfère executer l'outil quand même en utilisant la valeur "english" qu'il définit comme fallback.

### Exercice 2.1

```shell
$ python exercice_2_1.py "combien font 2 plus 2"
2 plus 2 font 4.

$ python exercice_2_1.py "combien font (2 + 2) * 8 + 4 (attention aux priorités de calcul) ?"
Pour calculer $(2 + 2) * 8 + 4$, nous devons suivre l'ordre des opérations (priorité des parenthèses d'abord) :

1. **Calcul dans les parenthèses :**
   $2 + 2 = 4$

2. **Multiplication :**
   $4 * 8 = 32$

3. **Addition :**
   $32 + 4 = 36$

Le résultat est **36**.
```

### Exercice 2.2

L'agent utilise correctement les 3 outils SQL et demande des tool calls pour ceux ci. Il répond également correctement aux 5 questions qu'on lui pose en ne dépassant pas les 5 itérations max.

Cependant, il peut arriver sur une certaine éxecution du script qu'il fail sur la question de l'auteur de Dune.

Il execute une mauvaise requête SQL qui lui renvoie une erreur SQL. Le LLM arrive a la prochaine itération a réexecuter la commande SQL corrigée (sans avoir encore ajouté le system prompt de l'exo 2.3) cependant il n'est pas capable de renvoyer le résultat à l'utilisateur car le tool call corrigé était la dernière itération. 

### Exercice 2.3




## Difficultés rencontrées

- La majeure difficulté que nous avons rencontrée à été de comprendre dans l'exo 1.2 qu'il fallait remplir correctement notre tableau messages avec la réponse du LLM demandant le tool call puis ensuite le message du tool call avec la réponse avant de redonner ce flux de messages au prochain appel de call_llm().

Une fois cela comprit, le TP est très bien guidé donc nous n'avons pas eu d'autres difficultés sur commment mettre en place la boucle de l'agent pour traiter plusieurs itérations. 

L'utilisation des dictionnaires python rend cela facile afin de checker les "finish reason" ou les "tools calls" pour les inclure dans nos conditions ou boucles python.

## Solutions apportées et résultats

- Voir réponses ci-dessus aux différents exercices.

## Réflexions

- Que pensez-vous du mécanisme de tool calling ?
- Quels sont les risques de sécurité d'un agent SQL ?
- Comment améliorer la gestion du contexte ?
- Quelles fonctionnalités vous sembleraient intéressantes d'ajouter ?
