import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Queue;


//made by Yi Ren for inf 552 2016 fall


//define the node of tree that suitable to use for this assignment
class TreeNode<T>{

    String data;
    TreeNode<String> parent;
    ArrayList<TreeNode<String>> children;
    ArrayList<String> eachValue;

    public TreeNode(String data) {
        this.data = data;
        this.children = new ArrayList<TreeNode<String>>();
        this.eachValue = new ArrayList<String>();
    }

}


public class DecisionTree {
	
	//read dt-data.txt and get the information of each record lines
	public ArrayList<ArrayList<String>> getData(String filePath) {
		ArrayList<ArrayList<String>> res = new ArrayList<ArrayList<String>>();
		try {
            String encoding="GBK";
            File file=new File(filePath);
            if(file.isFile() && file.exists()){ //whether file exist or not
                InputStreamReader read = new InputStreamReader(new FileInputStream(file),encoding);
                BufferedReader bufferedReader = new BufferedReader(read);
                int lineNum = 0;
                String linetxt = null;
                while((linetxt = bufferedReader.readLine()) != null) {
                	if (lineNum != 0 && lineNum != 1) {
                		ArrayList<String> listtmp = new ArrayList<String>(Arrays.asList(linetxt.split(":|;")));
                		ArrayList<String> list = new ArrayList<String>(Arrays.asList(listtmp.get(1).split(", ")));
                		res.add(list);
                		
                	}
                	lineNum++;
                }
                read.close();
            }
            else{
            	System.out.println("cannot find file");
            }
		} catch (Exception e) {
			System.out.println("error when read file");
			e.printStackTrace();
    	}
	return res;
	}
	
	//read dt-data.txt and get the attribute of first record lines
	public ArrayList<String> getAttribute(String filePath) {
		ArrayList<String> attribute = new ArrayList<String>();
		try {
            String encoding="GBK";
            File file=new File(filePath);
            if(file.isFile() && file.exists()){ //whether file exist or not
                InputStreamReader read = new InputStreamReader(new FileInputStream(file),encoding);
                BufferedReader bufferedReader = new BufferedReader(read);
                String linetxt = null;
                if ((linetxt = bufferedReader.readLine()) != null) {
                	String tmp = linetxt.substring(1, linetxt.length() - 1);
                	attribute = new ArrayList<String>(Arrays.asList(tmp.split(", ")));
                }
                read.close();
            }
            else{
            	System.out.println("cannot find file");
            	}
		} catch (Exception e) {
			System.out.println("error when read file");
			e.printStackTrace();
		}
		
	return attribute;
	}
	
	//calculate Entropy 
	public double calculateEntropy(ArrayList<ArrayList<String>> data) {
		int rowNum = data.size();
		int n = data.get(0).size() - 1;
		HashMap<String, Double> count = new HashMap<String, Double>();
		
		for (ArrayList<String> lineData : data) {
			if (!count.containsKey(lineData.get(n))) {
				count.put(lineData.get(n), 0.0);
			}
			count.put(lineData.get(n), count.get(lineData.get(n)) + 1);
		}
		
		double entropy = 0;
		for (String key : count.keySet() ) {
			entropy -= count.get(key)/rowNum * (Math.log(count.get(key)/rowNum) / Math.log(2));
		}
		
		return entropy;
	}
	
	//given records data and attribute, find all the branches of the attribute
	public ArrayList<String> getAttributeValueList(ArrayList<ArrayList<String>> data, int attributeIndex) {
		ArrayList<String> res = new ArrayList<String>();
		
		for (ArrayList<String> line : data) {
			if (!res.contains(line.get(attributeIndex))) {
				res.add(line.get(attributeIndex));
			}
		}
		
		return res;
	}
	
	//calculate information Gain for the given attribute
	public double calculateInfoGain(ArrayList<ArrayList<String>> data, int attributeIndex) {
		double infoGain = 0;
		ArrayList<String> valueList = new ArrayList<>(getAttributeValueList(data, attributeIndex));
		for (String s : valueList) {
			ArrayList<ArrayList<String>> subData = new ArrayList<>();
			double count = 0.0;
			for (ArrayList<String> line : data) {
				if (line.get(attributeIndex).equals(s)) {
					subData.add(line);
					count = count + 1;
				}
			}
			infoGain -= count/data.size() * calculateEntropy(subData);
		}
		return infoGain;
	}
	
	//find highest information gain attribute index, second for loop make tie attributes to choose first
	public int bestAttriToSplit(ArrayList<ArrayList<String>> data, ArrayList<String> attribute) {
		HashMap<Integer, Double> infoGain = new HashMap<>();
		
		for (int i = 0; i < attribute.size() - 1; i++) {
			infoGain.put(i, calculateInfoGain(data, i));
		}
		double maxValue = Double.NEGATIVE_INFINITY;
		int maxValueIndex = 0;
		for (int key : infoGain.keySet()) {
			if (infoGain.get(key) > maxValue) {
				maxValueIndex = key;
				maxValue = infoGain.get(key);
			}
		}
		
		return maxValueIndex;
	}
	
	//cut records lines by attribute and the branches of the attribute
	public ArrayList<ArrayList<String>> getUsefulData(ArrayList<ArrayList<String>> data, String value, int splitAttributeIndex) {
		ArrayList<ArrayList<String>> newData = new ArrayList<ArrayList<String>>();
		
		for (ArrayList<String> line : data) {
			if (line.get(splitAttributeIndex).equals(value)) {
				ArrayList<String> newEachData = new ArrayList<>(line);
				newEachData.remove(splitAttributeIndex);
				newData.add(newEachData);
			}
		}
		
		return newData;
	}
	
	//build decision tree, recursive
	public TreeNode<String> builtDecisionTree(ArrayList<ArrayList<String>> data, ArrayList<String> attribute) {
		if (data.size() == 0) {
			return null;
		}
		else if (calculateEntropy(data) == 0) {
			return new TreeNode<String>(data.get(0).get(data.get(0).size() - 1));
		}
		else {
			int splitAttributeIndex = bestAttriToSplit(data, attribute);
			String splitAttribute = attribute.get(splitAttributeIndex);
			TreeNode<String> node = new TreeNode<>(splitAttribute);
			attribute.remove(splitAttributeIndex);
			
			for (String eachValue : getAttributeValueList(data, splitAttributeIndex)) {
				ArrayList<ArrayList<String>> newData = getUsefulData(data, eachValue, splitAttributeIndex);
				ArrayList<String> newAttribute = new ArrayList<>(attribute);
				node.eachValue.add(eachValue);
				TreeNode<String> child = builtDecisionTree(newData, newAttribute);
				node.children.add(child);
			}
			return node;
		}
		
	}
	
	//print the tree layer by layer
	public void printTree (TreeNode<String> root) {
		Queue<TreeNode<String>> queue = new LinkedList<>();
		queue.add(root);
		ArrayList<ArrayList<String>> treeLevelElement = new ArrayList<ArrayList<String>>();
		ArrayList<String> level = new ArrayList<>();
		int curlevelElementNum = 1;
		int nextlevelElementNum = 0;
		
		while (!queue.isEmpty()) {
			TreeNode<String> node = queue.poll();
			level.add(node.data);
			nextlevelElementNum += node.children.size();
			if (level.size() == curlevelElementNum) {
				treeLevelElement.add(new ArrayList<>(level));
				level.clear();
				curlevelElementNum = nextlevelElementNum;
				nextlevelElementNum = 0;
			}
			
			for (TreeNode<String> child : node.children) {
				queue.add(child);
			}
			
		}
		for (ArrayList<String> layer : treeLevelElement) {
			for (String s : layer) {
				System.out.print(s + " ");
			}
			System.out.println();
		}
		
	}
	
	public TreeNode<String> decisionTree(ArrayList<String> attribute, ArrayList<ArrayList<String>> data) {
		TreeNode<String> root = builtDecisionTree(data, attribute);
		return root;
	}
	
	// test the case
	public String test(TreeNode<String> root, String[] testRecord, ArrayList<String> attributeToTestFun) {
		if (root.children.size() == 0) {
			return root.data;
		}
		int indexOfAttribute = attributeToTestFun.indexOf(root.data);
		String value = testRecord[indexOfAttribute];
		int indexOfValueInNode = 0;
		for (int i = 0; i < root.eachValue.size(); i++) {
			if (root.eachValue.get(i).equals(value)) {
				indexOfValueInNode = i;
				break;
			}
		}
		
		TreeNode<String> nextNode = root.children.get(indexOfValueInNode);
		String res = test(nextNode, testRecord, attributeToTestFun);
		return res;
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		String filePath = "/Users/renyi/Documents/workspace/INF552HW1V1/dt-data.txt";
		DecisionTree decisiontree = new DecisionTree();
        ArrayList<ArrayList<String>> data = decisiontree.getData(filePath);
        ArrayList<String> attribute = decisiontree.getAttribute(filePath);
        ArrayList<String> attributeToTestFun = new ArrayList<>(attribute.subList(0, attribute.size()));
        TreeNode<String> tree = decisiontree.decisionTree(attribute, data);
        decisiontree.printTree(tree);
        
        System.out.println();
        System.out.print("The result of the prediction is : ");
        String[] testRecord = {"Large", "Moderate", "Cheap", "Loud", "City-Center", "No", "No"};
        System.out.println(decisiontree.test(tree, testRecord, attributeToTestFun));
	}

}
